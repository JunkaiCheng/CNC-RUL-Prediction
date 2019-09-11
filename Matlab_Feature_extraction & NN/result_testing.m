
figure('color',[1 1 1])
y_test = myNeuralNetworkFunction_binary_0_99_134(feature_set_2)
plot(1:length(condition_set_2),condition_set_2,'-o')
hold on;
plot(1:length(y_test),y_test,'-o')
axis([0.9*length(y_test),length(y_test),0,1])
xlabel('piece # done');
ylabel('output')