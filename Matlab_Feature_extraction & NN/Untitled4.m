

data = table(C(:,2),C(end,2)-C(:,2),y');
writetable(data, 'tmp.csv') 