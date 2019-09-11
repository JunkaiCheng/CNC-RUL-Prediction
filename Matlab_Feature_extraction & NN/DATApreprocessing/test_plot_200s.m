figure('color',[1 1 1])
t=1/25600+80:1/25600:200;
plot(t,x1(80*25600+1:200*25600))
xlabel("time/s")
L=10000;

figure('color',[1 1 1])
t_sam = 80:0.01:150;
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
plot(80+0.01*[1:7001],-log10(1-R_square),'-')
ylabel('-log10(1-R)');
xlabel('time/s');
axis([-inf,150,-inf,inf])