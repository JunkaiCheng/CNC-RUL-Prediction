for id = 1:157
    feature = feature_set_4(id,:)';
    xx(id) = life_remain_4(id)
    for i = 1:length(threshold_set)
        %jud(i) = net_set{i}(encode(autoenc,feature));
        jud(i) = net_set{i}(feature);
    end
    yy(id) = find_thre(threshold_set, jud);
end
plot(xx,yy)