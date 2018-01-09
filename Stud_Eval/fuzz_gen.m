function [ y ] = fuzz_gen(x, type, par)
%UNTITLED2 Summary of this function goes here
%   Detailed explanation goes here

%y = zeros(1, numel(type))
for i = 1 : numel(type)
    
    if strcmp(type(i),'trap')
        y(:,i) = mf(x, par(i,:));
    elseif strcmp(type(i),'tri')
        y(:,i) = mf(x, par(i,1:3));
    else
        error('unknown input')
    end
    %clear x
end

end

