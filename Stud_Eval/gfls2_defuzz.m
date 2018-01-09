function [ crisp ] = gfls2_defuzz(alpha,x)
%glfs2_dfuzz is used to defuzzify MF into a crisp value
% get mf
x.mf = fuzz_gen(x.range, x.type, x.par);
for i = 1: numel(x.type)
    outmf(:,i) = alpha(i) * x.mf(:,i); % scalling
end
% aggregation
ag_mf = max(outmf,[],2);

%crisp =  defuzz(x.range,ag_mf,'centroid')
%crisp =  defuzz(x.range,ag_mf,'mom')
%crisp =  defuzz(x.range,ag_mf,'bisector')
%crisp =  defuzz(x.range,ag_mf,'som')
%crisp =  defuzz(x.range,ag_mf,'lom')

crisp = sum(ag_mf.*x.range')/sum(ag_mf); % centroid
end

