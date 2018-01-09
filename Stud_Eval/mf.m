function [ y ] = mf(x, par)
%mf: tri if numel of par = 3 and trp if 4
% for plotting: 
%     x = 0:0.1:5
%     y = mf( x, [1, 2, 3, 4])
%     y = mf( x, [1, 2, 3])
%     plot(x,y)
a = par(1);
b = par(2);
c = par(3);
if numel(par)==3
    y = max(min((x-a)/(b-a),(c-x)/(c-b)),0);  % tri
else
    d = par(4);
    y = max(min(min((x-a)/(b-a),(d-x)/(d-c)),1),0);  % trap
end
end

