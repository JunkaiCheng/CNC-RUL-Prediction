x = feature_set';

net_set = cell(1,length(threshold));
for i = 1 : length(threshold_set)
t = [condition_set_1{i};condition_set_2{i}; condition_set_3{i}]';
net_set{i} = patternnet(10, 'traingdx');
net_set{i} = train(net_set{i},x,t);
%y = net_set{i}(x);
end
%{
sta = 1;
fin = 164;
leng = fin - sta + 1;

plot(C1(sta:fin,2),t(sta:fin),'-o')
hold on;
plot(C1(sta:fin,2),y(sta:fin),'-o')
axis([-inf,inf,-inf,inf])
xlabel('piece # done');
ylabel('output')
%}