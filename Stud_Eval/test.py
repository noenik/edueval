import matplotlib
import numpy as np

matplotlib.use("Agg")

import skfuzzy as fuzz
from skfuzzy import control as ctrl

A = np.array([[0.59, 0.35, 1.00, 0.66, 0.11, 0.08, 0.84, 0.23, 0.04, 0.24],
              [0.01, 0.27, 0.14, 0.04, 0.88, 0.16, 0.04, 0.22, 0.81, 0.53],
              [0.77, 0.69, 0.97, 0.71, 0.17, 0.86, 0.87, 0.42, 0.91, 0.74],
              [0.73, 0.72, 0.18, 0.16, 0.50, 0.02, 0.32, 0.92, 0.90, 0.25],
              [0.93, 0.49, 0.08, 0.81, 0.65, 0.93, 0.39, 0.51, 0.97, 0.61]])

T = np.array([[0.7, 0.1, 0.1, 1.0, 0.7, 0.2, 0.7, 0.6, 0.4, 0.9],
              [1.0, 0.0, 0.9, 0.3, 1.0, 0.3, 0.2, 0.8, 0.0, 0.3],
              [0.0, 0.1, 0.0, 0.0, 0.9, 1.0, 0.2, 0.3, 0.1, 0.4],
              [0.2, 0.1, 0.0, 1.0, 1.0, 0.3, 0.4, 0.8, 0.7, 0.5],
              [0.0, 0.1, 1.0, 1.0, 0.6, 1.0, 0.8, 0.2, 0.8, 0.2]])

# C = matlab.double([[0.0, 0.85, 0.15, 0.0, 0.0],
#                    [0.0, 0.0, 0.33, 0.67, 0.0],
#                    [0.0, 0.0, 0.0, 0.69, 0.31],
#                    [0.56, 0.44, 0.0, 0.0, 0.0],
#                    [0.0, 0.0, 0.7, 0.3, 0.0]])

c = [.35, .6, .7, .2, .5]

i = [1, .3, .75, 0, .4]

# I = matlab.double([[0.0, 0.0, 0.0, 0.0, 1.0],
#                    [0.0, 0.33, 0.67, 0.0, 0.0],
#                    [0.0, 0.0, 0.0, 0.15, 0.85],
#                    [1.0, 0.0, 0.0, 0.0, 0.0],
#                    [0.0, 0.07, 0.93, 0.0, 0.0]])

G = [10, 15, 20, 25, 30]


# def run_evaluation(A, T, C, I, G):
#     eng = matlab.engine.start_matlab()
#     eng.addpath(os.path.dirname(os.path.abspath(__file__)))
#
#     A = matlab.double(A)
#     T = matlab.double(T)
#     # C = matlab.double(C)
#     # I = matlab.double(I)
#     G = matlab.double(G)
#
#     return eng.main(A, T, C, I, G)


def compile_difficulty():
    accuracy = ctrl.Antecedent(np.arange(0, 1.1, .1), 'accuracy')
    time = ctrl.Antecedent(np.arange(0, 1.1, .1), 'time')
    dif = ctrl.Consequent(np.arange(0, 1.1, .1), 'difficulty')

    accuracy['bad'] = fuzz.trapmf(accuracy.universe, [0, 0, .2, .4])
    accuracy['fair'] = fuzz.trimf(accuracy.universe, [.2, .5, .8])
    accuracy['excellent'] = fuzz.trapmf(accuracy.universe, [.6, .8, 1, 1])

    time['low'] = fuzz.trapmf(time.universe, [0, 0, .1, .3])
    time['medium'] = fuzz.trimf(time.universe, [.2, .4, .6])
    time['high'] = fuzz.trimf(time.universe, [.4, .6, .8])
    time['very high'] = fuzz.trapmf(time.universe, [.7, .9, 1, 1])

    dif['very low'] = fuzz.trapmf(dif.universe, [0, 0, .1, .3])
    dif['low'] = fuzz.trimf(dif.universe, [.1, .3, .5])
    dif['medium'] = fuzz.trimf(dif.universe, [.3, .5, .7])
    dif['high'] = fuzz.trimf(dif.universe, [.5, .7, .9])
    dif['very high'] = fuzz.trapmf(dif.universe, [.7, .9, 1, 1])

    rules = [ctrl.Rule(time['low'], dif['low']),
             ctrl.Rule(accuracy['bad'], dif['low']),
             ctrl.Rule(accuracy['bad'] & time['low'], dif['very low']),
             ctrl.Rule(accuracy['bad'] & time['medium'], dif['low']),
             ctrl.Rule(accuracy['bad'] & time['high'], dif['medium']),
             ctrl.Rule(accuracy['bad'] & time['very high'], dif['high']),
             ctrl.Rule(accuracy['fair'] & time['low'], dif['low']),
             ctrl.Rule(accuracy['fair'] & time['medium'], dif['medium']),
             ctrl.Rule(accuracy['fair'] & time['high'], dif['high']),
             ctrl.Rule(accuracy['fair'] & time['very high'], dif['very high']),
             ctrl.Rule(accuracy['excellent'] & time['low'], dif['medium']),
             ctrl.Rule(accuracy['excellent'] & time['medium'], dif['high']),
             ctrl.Rule(accuracy['excellent'] & time['high'], dif['very high']),
             ctrl.Rule(accuracy['excellent'] & time['very high'], dif['very high']),
             ]

    dif_ctrl = ctrl.ControlSystem(rules)

    return ctrl.ControlSystemSimulation(dif_ctrl)


def compile_effort(mf):
    dif = ctrl.Antecedent(np.arange(0, 1.1, .1), 'difficulty')
    complexity = ctrl.Antecedent(np.arange(0, 1.1, .1), 'complexity')
    eff = ctrl.Consequent(np.arange(0, 1.1, .1), 'effort')

    dif['very low'] = fuzz.trapmf(dif.universe, [0, 0, .1, .3])
    dif['low'] = fuzz.trimf(dif.universe, [.1, .3, .5])
    dif['medium'] = fuzz.trimf(dif.universe, [.3, .5, .7])
    dif['high'] = fuzz.trimf(dif.universe, [.5, .7, .9])
    dif['very high'] = fuzz.trapmf(dif.universe, [.7, .9, 1, 1])

    complexity['very low'] = fuzz.trapmf(complexity.universe, mf[0])  # [0, 0, .1, .3])
    complexity['low'] = fuzz.trimf(complexity.universe, mf[1])  # [.1, .3, .5])
    complexity['medium'] = fuzz.trimf(complexity.universe, mf[2])  # [.3, .5, .7])
    complexity['high'] = fuzz.trimf(complexity.universe, mf[3])  # [.5, .7, .9])
    complexity['very high'] = fuzz.trapmf(complexity.universe, mf[4])  # [.7, .9, 1, 1])

    eff['low'] = fuzz.trapmf(eff.universe, [0, 0, .1, .3])
    eff['medium'] = fuzz.trimf(eff.universe, [.2, .4, .6])
    eff['high'] = fuzz.trimf(eff.universe, [.4, .6, .8])
    eff['very high'] = fuzz.trapmf(eff.universe, [.7, .9, 1, 1])

    rules = [ctrl.Rule(dif['very low'] & complexity['very low'], eff['low']),
             ctrl.Rule(dif['very low'] & complexity['low'], eff['low']),
             ctrl.Rule(dif['very low'] & complexity['medium'], eff['low']),
             ctrl.Rule(dif['very low'] & complexity['high'], eff['medium']),
             ctrl.Rule(dif['very low'] & complexity['very high'], eff['high']),
             ctrl.Rule(dif['low'] & complexity['very low'], eff['low']),
             ctrl.Rule(dif['low'] & complexity['low'], eff['low']),
             ctrl.Rule(dif['low'] & complexity['medium'], eff['medium']),
             ctrl.Rule(dif['low'] & complexity['high'], eff['high']),
             ctrl.Rule(dif['low'] & complexity['very high'], eff['high']),
             ctrl.Rule(dif['medium'] & complexity['very low'], eff['low']),
             ctrl.Rule(dif['medium'] & complexity['low'], eff['low']),
             ctrl.Rule(dif['medium'] & complexity['medium'], eff['medium']),
             ctrl.Rule(dif['medium'] & complexity['high'], eff['high']),
             ctrl.Rule(dif['medium'] & complexity['very high'], eff['high']),
             ctrl.Rule(dif['high'] & complexity['very low'], eff['medium']),
             ctrl.Rule(dif['high'] & complexity['low'], eff['medium']),
             ctrl.Rule(dif['high'] & complexity['medium'], eff['high']),
             ctrl.Rule(dif['high'] & complexity['high'], eff['high']),
             ctrl.Rule(dif['high'] & complexity['very high'], eff['very high']),
             ctrl.Rule(dif['very high'] & complexity['very low'], eff['medium']),
             ctrl.Rule(dif['very high'] & complexity['low'], eff['high']),
             ctrl.Rule(dif['very high'] & complexity['medium'], eff['high']),
             ctrl.Rule(dif['very high'] & complexity['high'], eff['very high']),
             ctrl.Rule(dif['very high'] & complexity['very high'], eff['very high']),
             ]

    eff_ctrl = ctrl.ControlSystem(rules)

    return ctrl.ControlSystemSimulation(eff_ctrl)


def compile_adjustment(mf):
    eff = ctrl.Antecedent(np.arange(0, 1.1, .1), 'effort')
    importance = ctrl.Antecedent(np.arange(0, 1.1, .1), 'importance')
    adj = ctrl.Consequent(np.arange(0, 1.1, .1), 'adjustment')

    eff['low'] = fuzz.trapmf(eff.universe, [0, 0, .1, .3])
    eff['medium'] = fuzz.trimf(eff.universe, [.2, .4, .6])
    eff['high'] = fuzz.trimf(eff.universe, [.4, .6, .8])
    eff['very high'] = fuzz.trapmf(eff.universe, [.7, .9, 1, 1])

    importance['very low'] = fuzz.trapmf(importance.universe, mf[0])  # [0, 0, .1, .3])
    importance['low'] = fuzz.trimf(importance.universe, mf[1])  # [.1, .3, .5])
    importance['medium'] = fuzz.trimf(importance.universe, mf[2])  # [.3, .5, .7])
    importance['high'] = fuzz.trimf(importance.universe, mf[3])  # [.5, .7, .9])
    importance['very high'] = fuzz.trapmf(importance.universe, mf[4])  # [.7, .9, 1, 1])

    adj['very low'] = fuzz.trapmf(adj.universe, [0, 0, .1, .3])
    adj['low'] = fuzz.trimf(adj.universe, [.1, .3, .5])
    adj['medium'] = fuzz.trimf(adj.universe, [.3, .5, .7])
    adj['high'] = fuzz.trimf(adj.universe, [.5, .7, .9])
    adj['very high'] = fuzz.trapmf(adj.universe, [.7, .9, 1, 1])

    rules = [ctrl.Rule(eff['low'] & importance['very low'], adj['low']),
             ctrl.Rule(eff['low'] & importance['low'], adj['low']),
             ctrl.Rule(eff['low'] & importance['medium'], adj['medium']),
             ctrl.Rule(eff['low'] & importance['high'], adj['high']),
             ctrl.Rule(eff['low'] & importance['very high'], adj['high']),
             ctrl.Rule(eff['medium'] & importance['very low'], adj['low']),
             ctrl.Rule(eff['medium'] & importance['low'], adj['low']),
             ctrl.Rule(eff['medium'] & importance['medium'], adj['medium']),
             ctrl.Rule(eff['medium'] & importance['high'], adj['high']),
             ctrl.Rule(eff['medium'] & importance['very high'], adj['high']),
             ctrl.Rule(eff['high'] & importance['very low'], adj['medium']),
             ctrl.Rule(eff['high'] & importance['low'], adj['medium']),
             ctrl.Rule(eff['high'] & importance['medium'], adj['high']),
             ctrl.Rule(eff['high'] & importance['high'], adj['high']),
             ctrl.Rule(eff['high'] & importance['very high'], adj['very high']),
             ctrl.Rule(eff['very high'] & importance['very low'], adj['medium']),
             ctrl.Rule(eff['very high'] & importance['low'], adj['high']),
             ctrl.Rule(eff['very high'] & importance['medium'], adj['high']),
             ctrl.Rule(eff['very high'] & importance['high'], adj['very high']),
             ctrl.Rule(eff['very high'] & importance['very high'], adj['very high']),
             ]

    adj_ctrl = ctrl.ControlSystem(rules)

    return ctrl.ControlSystemSimulation(adj_ctrl)


def compile_rulebases(mfs):
    return {'difficulty': compile_difficulty(),
            'effort': compile_effort(mfs['Complexity']),
            'adjustment': compile_adjustment(mfs['Importance'])}


def infer_difficulty(acc, time, rbs):
    rb = rbs['difficulty']
    rb.input['accuracy'] = acc
    rb.input['time'] = time

    rb.compute()
    return rb.output['difficulty']


def infer_effort(diff, cmplx, rbs):
    rb = rbs['effort']
    rb.input['difficulty'] = diff
    rb.input['complexity'] = cmplx

    rb.compute()
    return rb.output['effort']


def infer_adjustment(eff, imp, rbs):
    rb = rbs['adjustment']
    rb.input['effort'] = eff
    rb.input['importance'] = imp

    rb.compute()
    return rb.output['adjustment']


# rbs = compile_rulebases()


def evaluate(w, t, cmplx, imp, rbs, a=None):
    new_w = []

    if not a:
        a = A

    for i in range(a.shape[0]):
        acc = sum(a[i, :].tolist())/a.shape[1]
        time = sum([1-l for l in t[i, :].tolist()])/a.shape[1]
        cm = cmplx[i]
        im = imp[i]

        diff = infer_difficulty(acc, time, rbs)
        effort = infer_effort(diff, cm, rbs)
        adjustment = infer_adjustment(effort, im, rbs)

        new_w.append((1 + adjustment) * w[i])

    m = sum(w) / sum(new_w)

    new_w = [i * m for i in new_w]

    return new_w


if __name__ == '__main__':
    # new_w = np.zeros((A.shape[0], A.shape[1]))
    # print(A.shape[0])

    # ar = np.array([[1, 2, 3],
    #                [4, 5, 6]])
    # print(ar.shape[1])

    kek = evaluate(A, T, c, i)
    # lel = np.apply_along_axis(lambda x: sum(x), axis=0, arr=kek)

    print(kek)
    print()

    print(run_evaluation(A.tolist(), T.tolist(), C, I, G))
