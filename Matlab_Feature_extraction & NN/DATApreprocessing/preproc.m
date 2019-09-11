load('raw_data.mat')

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

figure('color',[1 1 1])
t=1/25600:1/25600:240;
plot(t,x1(1:5120000))
xlabel("time/s")
L=10000;

figure('color',[1 1 1])
t_sam = 60:0.01:240;
x_max=zeros(1,length(t_sam));
for i=1:length(t_sam)
   center = floor(t_sam(i)*25600);
   x_max(i)=sum(abs(x1(center-10000:center)))/L;
end
plot(t_sam,x_max)
xlabel("time/s")

figure('color',[1 1 1])
R_square = zeros(1, length(x_max-38));
for i=1:length(x_max)-38
    corr = corrcoef(x_max(i:i+38)',[1:39]');
    R_square(i) = corr(2,1)^2;
end
R_log = -log10(1-R_square);
plot(60+0.01*[1:9001],-log10(1-R_square),'-')
ylabel('-log10(1-R)');
xlabel('time/s');
