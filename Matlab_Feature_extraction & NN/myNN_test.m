figure('color',[1 1 1])
id = 153;
feature = feature_set_1(id,:)';
life_remain_1(id)
for i = 1:length(threshold_set)
    %jud(i) = net_set{i}(encode(autoenc,feature));
    jud(i) = net_set{i}(feature);
end
plot(threshold_set,jud,'o')
xlabel('RUL<?')
title('200 classification results based on data with RUL=5');
res = find_thre(threshold_set, jud)

figure('color',[1 1 1])
id = 150;
feature = feature_set_1(id,:)';
life_remain_1(id)
for i = 1:length(threshold_set)
        %jud(i) = net_set{i}(encode(autoenc,feature));
    jud(i) = net_set{i}(feature);
end
plot(threshold_set,jud,'o')
xlabel('RUL<?')
title('200 classification results based on data with RUL=10');
res = find_thre(threshold_set, jud)

figure('color',[1 1 1])
id = 144;
feature = feature_set_1(id,:)';
life_remain_1(id)
for i = 1:length(threshold_set)
    %jud(i) = net_set{i}(encode(autoenc,feature));
    jud(i) = net_set{i}(feature);
end
plot(threshold_set,jud,'o')
xlabel('RUL<?')
title('200 classification results based on data with RUL=20');
res = find_thre(threshold_set, jud)

figure('color',[1 1 1])
id = 132;
feature = feature_set_1(id,:)';
life_remain_1(id)
for i = 1:length(threshold_set)
    %jud(i) = net_set{i}(encode(autoenc,feature));
    jud(i) = net_set{i}(feature);
end
plot(threshold_set,jud,'o')
xlabel('RUL<?')
title('200 classification results based on data with RUL=50');
res = find_thre(threshold_set, jud)
%{
sta = 1;
fin = 157;
leng = fin - sta + 1;
feature = feature_set_4';
y = net_set{2}(encode(autoenc,feature));
t = condition_set_4{2};
x = C4(sta:fin,2);

plot(x,t,'-o')
hold on;
plot(x,y,'-o')
axis([-inf,inf,-inf,inf])
xlabel('piece # done');
ylabel('output')
%}