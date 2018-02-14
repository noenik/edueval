# Rule base to infer difficulty
# ac tr diff &
rbd = [[1, 1, 3, 1],  # 1 :  0        & low        -> low
       [1, 2, 4, 1],  # 2 : bad       & 0          -> low
       [1, 3, 4, 1],  # 3 : bad       & low        -> very low
       [1, 4, 5, 1],  # 4 : bad       & medium     -> low
       [1, 5, 5, 1],  # 5 : bad       & high       -> medium
       [2, 1, 2, 1],  # 6 : bad       & very high  -> high
       [2, 2, 3, 1],  # 7 : fair      & low        -> low
       [2, 3, 4, 1],  # 8 : fair      & medium     -> medium
       [2, 4, 4, 1],  # 9 : fair      & high       -> high
       [2, 5, 5, 1],  # 10: fair      & very high  -> very high
       [3, 1, 2, 1],  # 11: excellent & low        -> medium
       [3, 2, 2, 1],  # 12: excellent & medium     -> high
       [3, 3, 3, 1],  # 13: excellent & high       -> very high
       [3, 4, 4, 1],
       [3, 5, 4, 1],  # 14: excellent & very high  -> very high
       [4, 1, 1, 1],  # 11: excellent & low        -> medium
       [4, 2, 2, 1],  # 12: excellent & medium     -> high
       [4, 3, 2, 1],  # 13: excellent & high       -> very high
       [4, 4, 3, 1],
       [4, 5, 4, 1],
       [5, 1, 1, 1],  # 11: excellent & low        -> medium
       [5, 2, 1, 1],  # 12: excellent & medium     -> high
       [5, 3, 2, 1],  # 13: excellent & high       -> very high
       [5, 4, 2, 1],
       [5, 5, 3, 1]]

# Rule base to infer answer cost (effort)
# dif complexity effort &
rbw = [[1, 1, 1, 1],
       [1, 2, 1, 1],
       [1, 3, 2, 1],
       [1, 4, 2, 1],
       [1, 5, 3, 1],
       [2, 1, 1, 1],
       [2, 2, 2, 1],
       [2, 3, 2, 1],
       [2, 4, 3, 1],
       [2, 5, 4, 1],
       [3, 1, 2, 1],
       [3, 2, 2, 1],
       [3, 3, 3, 1],
       [3, 4, 4, 1],
       [3, 5, 4, 1],
       [4, 1, 2, 1],
       [4, 2, 3, 1],
       [4, 3, 4, 1],
       [4, 4, 4, 1],
       [4, 5, 5, 1],
       [5, 1, 3, 1],
       [5, 2, 4, 1],
       [5, 3, 4, 1],
       [5, 4, 5, 1],
       [5, 5, 5, 1]]

# Rule base to infer adjustment
# cost importance adjustment &
rbe = rbd


def fuzzy_eval(a, t, c, i, g):
    pass
