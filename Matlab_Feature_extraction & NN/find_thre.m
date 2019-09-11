function [thres] = find_thre(x,y)
    for i=1:length(x)
        refmax = x>x(i);
        value(i) = sum((y-refmax).^2);
    end
    pos = find(value == min(value));
    thres = x(pos);
end