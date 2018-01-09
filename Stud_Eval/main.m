function mainv = main(A, T, C, I, G)
%% test my gfls: student evaluation
%clear all
%clc
% define variables
% try bell shaped memership functions gbellmf(x, [a b c])
% (1) accuracy rate of student i in question j
%A = [0.59 0.35 1.00 0.66 0.11 0.08 0.84 0.23 0.04 0.24;
%    0.01 0.27 0.14 0.04 0.88 0.16 0.04 0.22 0.81 0.53;
%    0.77 0.69 0.97 0.71 0.17 0.86 0.87 0.42 0.91 0.74;
%    0.73 0.72 0.18 0.16 0.50 0.02 0.32 0.92 0.90 0.25;
%    0.93 0.49 0.08 0.81 0.65 0.93 0.39 0.51 0.97 0.61];

Aav = mean(A,2);
n = numel(Aav);  % number of exam questions

aij = struct('name','accuracy rate',...
    'range',[0:0.01:1],...
    'val', [],...
    'type',{{'trap' 'tri' 'tri' 'tri' 'trap'}},...
    'par', [0 0 0.1 0.3;
    0.1 0.3 0.5 0;
    0.3 0.5 0.7 0;
    0.5 0.7 0.9 0;
    0.7 0.9 1.0 1.0]);

% (2) time rate of student i in question j
%T = [0.7 0.1 0.1 1.0 0.7 0.2 0.7 0.6 0.4 0.9;
%    1.0 0.0 0.9 0.3 1.0 0.3 0.2 0.8 0.0 0.3;
%    0.0 0.1 0.0 0.0 0.9 1.0 0.2 0.3 0.1 0.4;
%    0.2 0.1 0.0 1.0 1.0 0.3 0.4 0.8 0.7 0.5;
%    0.0 0.1 1.0 1.0 0.6 1.0 0.8 0.2 0.8 0.2];

Tav = mean(T,2);

tij = aij;
tij.name='time rate';

% (3) complexity
%C = [0.0  0.85 0.15 0.0  0.0;
%    0.0  0.0  0.33 0.67 0.0;
%    0.0  0.0  0.0  0.69 0.31;
%    0.56 0.44 0.0  0.0  0.0;
%    0.0  0.0  0.7  0.3  0.0];
Cj = aij;
Cj.name = 'complexity';
Cav = zeros(n,1);
for i = 1 : n
    Cav(i) = gfls2_defuzz(C(i,:),Cj);
end
% (4) importance of question i in level k: Iik
%{
I = [0.0 0.0  0.0  0.0  1.0;
    0.0 0.33 0.67 0.0  0.0;
    0.0 0.0  0.0  0.15 0.85;
    1.0 0.0  0.0  0.0  0.0;
    0.0 0.07 0.93 0.0  0.0];
%}
Ij = aij;
Ij.name = 'importance';
Iav = zeros(n,1);
for i = 1 : numel(Ij.type)
    Iav(i) = gfls2_defuzz(I(i,:),Ij);
end
%x.mf = fuzz_gen(Iav(1), Ij.type, Ij.par)
% (5) difficulty
Dj = aij;
Dj.name = 'difficulty';

% (6) effort
Ej = aij;
Ej.name = 'effort';

% (7) adjustment
Wj = aij;
Wj.name = 'adjustment';

%% rule bases:
% rule base: to infear difficulty
%ac tr dif &
RBD = [1 1 3 1;     %1 :  0        & low        -> low
    1 2 4 1;     %2 : bad       & 0          -> low
    1 3 4 1;     %3 : bad       & low        -> very low
    1 4 5 1;     %4 : bad       & medium     -> low
    1 5 5 1;     %5 : bad       & high       -> medium
    2 1 2 1;     %6 : bad       & very high  -> high
    2 2 3 1;     %7 : fair      & low        -> low
    2 3 4 1;     %8 : fair      & medium     -> medium
    2 4 4 1;     %9 : fair      & high       -> high
    2 5 5 1;     %10: fair      & very high  -> very high
    3 1 2 1;     %11: excellent & low        -> medium
    3 2 2 1;     %12: excellent & medium     -> high
    3 3 3 1;     %13: excellent & high       -> very high
    3 4 4 1;
    3 5 4 1;      %14: excellent & very high  -> very high
    4 1 1 1;     %11: excellent & low        -> medium
    4 2 2 1;     %12: excellent & medium     -> high
    4 3 2 1;     %13: excellent & high       -> very high
    4 4 3 1;
    4 5 4 1;
    5 1 1 1;     %11: excellent & low        -> medium
    5 2 1 1;     %12: excellent & medium     -> high
    5 3 2 1;     %13: excellent & high       -> very high
    5 4 2 1;
    5 5 3 1;];

%Rulebase to infer answer cost (effort)
%dif complex effort &
RBW = [1 1 1 1;
    1 2 1 1;
    1 3 2 1;
    1 4 2 1;
    1 5 3 1;
    2 1 1 1;
    2 2 2 1;
    2 3 2 1;
    2 4 3 1;
    2 5 4 1;
    3 1 2 1;
    3 2 2 1;
    3 3 3 1;
    3 4 4 1;
    3 5 4 1;
    4 1 2 1;
    4 2 3 1;
    4 3 4 1;
    4 4 4 1;
    4 5 5 1;
    5 1 3 1;
    5 2 4 1;
    5 3 4 1;
    5 4 5 1;
    5 5 5 1;
    ];

% rule base to infer adjustment
%cost importance adjustment &
RBE = RBD;

%      %hv inc int app cr  &
% RB3 = [0  1   2   0   1  1;         %1 :  0        & low        -> low
%        0  1   3   0   1  1;     %2 : bad       & 0          -> low
%        0  2   3   0   2  1;     %3 : bad       & low        -> very low
%        0  0   0   1   1  1;     %4 : bad       & medium     -> low
%        1  0   0   0   1  1;     %5 : bad       & high       -> medium
%        1  0   0   2   2  1;     %6 : bad       & very high  -> high
%        2  0   0   2   2  1;     %7 : fair      & low        -> low
%        3  0   0   2   3  1;     %8 : fair      & medium     -> medium
%        4  0   0   2   4  1;     %9 : fair      & high       -> high
%        5  0   0   2   4  1;     %10: fair      & very high  -> very high
%        1  0   0   3   2  1;     %11: excellent & low        -> medium
%        2  0   0   3   3  1;     %12: excellent & medium     -> high
%        3  0   0   3   4  1;     %13: excellent & high       -> very high
%        4  0   0   3   4  1;     %14: excellent & very high  -> very high
%        5  0   0   3   5  1;     %15: excellent & very high  -> very high
%        ];

%%
% find difficulty
tic
mamd = 0;
D = [];
E = [];
W = [];
for i = 1 : n
    % diff node
    aij.val = Aav(i);
    tij.val = Tav(i);
    Dj.val  = gfls2([aij,tij,Dj], RBD, mamd);
    D = [D; Dj.val];
    
    % effort node
    Cj.val = Cav(i);
    Ej.val = gfls2([Dj,Cj,Ej], RBE, mamd);
    E = [E; Ej.val];
    
    % Adjustment node
    Ij.val = Iav(i);
    Wj.val = gfls2([Ej,Ij,Wj], RBW, mamd);
    W = [W; Wj.val];
    
end
toc
%% update grade vector
%G = [10 15 20 25 30];
ws = zscore(W+1);

Gnew = G'.*(1+W);
Gnew = Gnew * sum(G)/sum(Gnew);
mainv = Gnew;
%sum(Gnew)
%% test to get new total score
S = Gnew'*A;                                 % 0 <= W <= 1   so  G <= G1 <= 2G

%% 3D plot for RBD
%{
[X,Y] = meshgrid(aij.range, tij.range);
%Z = sugeno(X,Y);
[m n] = size(X);
steps = m*n;

h = waitbar(0,'Please wait...');
for i = 1 : m
    for j = 1 : n
        aij.val = X(i,j);
        tij.val = Y(i,j);
        Z(i,j) = gfls2([aij,tij,Dj], RBD, mamd);
    end
    waitbar(i/m)
end
close(h)

%cla reset
figure
surf(X,Y,Z)
xlabel('Accuracy rate')
ylabel('Answer time')
zlabel('Difficulty')

%% 3D plot for RBE
[X,Y] = meshgrid(Dj.range, Cj.range);
%Z = sugeno(X,Y);
[m n] = size(X);
steps = m*n;

h = waitbar(0,'Please wait...');
for i = 1 : m
    for j = 1 : n
        Dj.val = X(i,j);
        Cj.val = Y(i,j);
        Z(i,j) = gfls2([Dj,Cj,Ej], RBE, mamd);
    end
    waitbar(i/m)
end
close(h)

%colormap default %winter
%waterfall(Y,X,Z)
%plot3(X,Y,Z)
figure
surf(X,Y,Z)
xlabel('Difficulty')
ylabel('Complexity')
zlabel('Answer-cost')

%% 3D plot for RBW
[X,Y] = meshgrid(Ej.range, Ij.range);
%Z = sugeno(X,Y);
[m n] = size(X);
steps = m*n;

h = waitbar(0,'Please wait...');
for i = 1 : m
    for j = 1 : n
        Ej.val = X(i,j);
        Ij.val = Y(i,j);
        Z(i,j) = gfls2([Ej,Ij,Wj], RBW, mamd);
    end
    waitbar(i/m)
end
close(h)

%colormap default %winter
%waterfall(Y,X,Z)
%plot3(X,Y,Z)
figure
surf(X,Y,Z)
xlabel('Answer-cost')
ylabel('Importance')
zlabel('Adjustment')
%}