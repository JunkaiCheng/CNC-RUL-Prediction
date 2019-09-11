load('C1.mat')
[r,c] = size(C1);
time_final = C1(r,2);
life_remain = time_final - C1(:,2);
feature_set = C1(:,3:100);
