x = feature_set';
autoenc = trainAutoencoder(x,100,'TrainingAlgorithm','trainscg')
x = encode(autoenc,x);