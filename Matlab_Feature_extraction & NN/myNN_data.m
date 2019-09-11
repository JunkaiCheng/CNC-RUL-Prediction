clear all
clc

load('C1.mat')
load('C2.mat')
load('C3.mat')
load('C4.mat')

[r1,c1] = size(C1);
life_remain_1 = C1(r1,2) - C1(:,2);
feature_set_1 = C1(:,3:end);
[r2,c2] = size(C2);
life_remain_2 = C2(r2,2) - C2(:,2);
feature_set_2 = C2(:,3:end);
[r3,c3] = size(C3);
life_remain_3 = C3(r3,2) - C3(:,2);
feature_set_3 = C3(:,3:end);
[r4,c4] = size(C4);
life_remain_4 = C4(r4,2) - C4(:,2);
feature_set_4 = C4(:,3:end);

threshold_set = [1:200];
condition_set_1 = cell(1,length(threshold_set));
condition_set_2 = cell(1,length(threshold_set));
condition_set_3 = cell(1,length(threshold_set));
condition_set_4 = cell(1,length(threshold_set));
for i = 1 : length(threshold_set)
    threshold = threshold_set(i);
    condition_set_1{i} = (life_remain_1 <= threshold);
    condition_set_2{i} = (life_remain_2 <= threshold);
    condition_set_3{i} = (life_remain_3 <= threshold);
    condition_set_4{i} = (life_remain_4 <= threshold);
end

feature_set = [feature_set_1 ;feature_set_2; feature_set_3];