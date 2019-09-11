for i=1:164
    [Y,~,~]=myNeuralNetworkFunction(feature_set(i,:))
    res(i)=Y;
end