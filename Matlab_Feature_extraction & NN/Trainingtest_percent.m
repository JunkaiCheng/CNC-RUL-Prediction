load('C1.mat')
load('C2.mat')
load('C3.mat')
load('C4.mat')
threshold = 0.99;
[r1,c1] = size(C1);
time_final = C1(r1,2);
life_remain_1 = time_final - C1(:,2);
feature_set_1 = C1(:,3:end);
process_percentage = C1(:,2)/C1(end,2);
%condition_classify = (process_percentage>=0.8)+(process_percentage>=0.5)+(process_percentage>=0.2)+(process_percentage>=0.1);
condition_classify = (process_percentage>=threshold);
condition_set_1 = condition_classify;

[r2,c2] = size(C2);
time_final = C2(r2,2);
life_remain_2 = time_final - C2(:,2);
feature_set_2 = C2(:,3:end);
process_percentage = C2(:,2)/C2(end,2);
%condition_classify = (process_percentage>=0.8)+(process_percentage>=0.5)+(process_percentage>=0.2)+(process_percentage>=0.1);
condition_classify = (process_percentage>=threshold);
condition_set_2 = condition_classify;

[r3,c3] = size(C3);
time_final = C3(r3,2);
life_remain_3 = time_final - C3(:,2);
feature_set_3 = C3(:,3:end);
process_percentage = C3(:,2)/C3(end,2);
%condition_classify = (process_percentage>=0.8)+(process_percentage>=0.5)+(process_percentage>=0.2)+(process_percentage>=0.1);
condition_classify = (process_percentage>=threshold);
condition_set_3 = condition_classify;


[r4,c4] = size(C4);
time_final = C4(r4,2);

life_remain_4 = time_final - C4(:,2);
feature_set_4 = C4(:,3:end);
process_percentage = C4(:,2)/C4(end,2);
%condition_classify = (process_percentage>=0.8)+(process_percentage>=0.5)+(process_percentage>=0.2)+(process_percentage>=0.1);
condition_classify = (process_percentage>=threshold);
condition_set_4 = condition_classify;

life_remain = [life_remain_1;life_remain_3;life_remain_4];
feature_set = [feature_set_1;feature_set_3;feature_set_4];
condition_set = [condition_set_1;condition_set_3;condition_set_4];