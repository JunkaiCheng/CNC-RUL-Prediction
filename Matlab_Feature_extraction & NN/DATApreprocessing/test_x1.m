x1=zeros(1,1800*25600);
for i=0:1799
    for j=1:25600
        if data{i+1,1}==0
            x1(i*25600+j)=0;
        else
            x1(i*25600+j)=data{i+1,2}(1,j);
        end
    end
end