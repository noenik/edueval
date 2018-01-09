function [crisp] = gfls2(x, R,mamd)
%general Mamdani FLS has two crisp inputs: x and y and one crisp output: z
%% fuzzify inputs AND output
for i = 1 : numel(x)
    if i == numel(x)
        x(i).mf = fuzz_gen(x(i).range, x(i).type, x(i).par);
    else
        x(i).mf = fuzz_gen(x(i).val, x(i).type, x(i).par);
    end
end
%% find index of rules use OR and AND
[r c] = size(R);
L = logical(R);

and_idx =  L(:,c);
or_idx  = ~L(:,c);

zero_idx = logical(ones(r,1));

for i = 1 : c-2
    zero_idx = zero_idx .* L(:,i);
end

alpha = zeros(r,1);
alpha(find(and_idx)) = 1;  % to get min correctly
%alpha = L(:,c);
% firing strength
for i = 1 : r
    if zero_idx(i) & and_idx(i)
        for j = 1 : c-2
            alpha(i) = min(alpha(i), x(j).mf(R(i,j)));   % and
        end
    elseif zero_idx(i) & or_idx(i)
        for j = 1 : c-2
            alpha(i) = max(alpha(i), x(j).mf(R(i,j)));    % or
        end
    elseif ~zero_idx(i)
        nonzero_idx = find(L(i,1:c-2));
        if and_idx(i)
            for j = 1 : numel(nonzero_idx)
                alpha(i) = min(alpha(i), x(nonzero_idx(j)).mf(R(i,nonzero_idx(j))));   % and
            end
        else
            for j = 1 : numel(nonzero_idx)
                alpha(i) = max(alpha(i), x(nonzero_idx(j)).mf(R(i,nonzero_idx(j))));    % or
            end
        end
        
    end
end

% reduce alpha to number of output MFs
alpha_max = zeros(numel(x(c-1).type),1);
for i = 1 : numel(x(c-1).type)
    alpha_max(i) = max(alpha(find(R(:,c-1)==i)));
end

%% defuzzification
if mamd
    %% implication
    im_z = implication(x(c-1).mf, alpha_max, 'clip');
    
    %% aggregation
    ag_z = max(im_z,[],2);
    %hold on
    %figure
    %plot(im_z)
    %plot(ag_z)
    
    crisp = sum(ag_z.*x(c-1).range')/sum(ag_z);
else
    K = mean(x(end).par');
    crisp = sum(alpha_max.*K')/sum(alpha_max);
end
end