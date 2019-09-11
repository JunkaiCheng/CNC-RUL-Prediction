%{
figure('color',[1 1 1])
subplot(2,2,1)
t=1/25600:1/25600:240;
plot(t,x1(1:6144000))
xlabel("time/s")
L=10000;

subplot(2,2,2)
t_sam = 60:0.01:240;
x_max=zeros(1,length(t_sam));
for i=1:length(t_sam)
   center = floor(t_sam(i)*25600);
   x_max(i)=sum(abs(x1(center-10000:center)))/L;
end
plot(t_sam,x_max)
xlabel("time/s")

subplot(2,2,3)
R_square = zeros(1, length(x_max-38));
for i=1:length(x_max)-38
    corr = corrcoef(x_max(i:i+38)',[1:39]');
    R_square(i) = corr(2,1)^2;
end
R_log = -log10(1-R_square);
plot(60+0.01*[1:18001],-log10(1-R_square),'-')
hold on
plot(60+0.01*timeset,R_log(timeset),'ro')
for i=1:length(timeset)
    isodd = mod(i,2);
    text(60+0.01*timeset(i)+0.2,R_log(timeset(i))+0.1,char(68*isodd+65*(1-isodd)),'fontsize',6);
end
ylabel('-log10(1-R)');
xlabel('time/s');
%}
%{
timeset=[];
for i=2:length(R_log)-1
   if R_log(i)>2&&R_log(i)>R_log(i-1)&&R_log(i)>R_log(i-2)&&R_log(i)>R_log(i+1)&&R_log(i)>R_log(i+2)&&R_log(i)>R_log(i-4)&&R_log(i)>R_log(i+4)
        timeset = [timeset i];
   end
end
%}

R_2 = -log10(1-R_square);
for i=60:120
    figure('color',[1 1 1])
    subplot(2,2,1)
    t=1/25600:1/25600:i;
    plot(t,x1(1:25600*i))
    xlabel("time/s")
    ylabel("Raw Data")
    axis([60,120,-6,6])
    title("Figure 1: Raw data")
    
    subplot(2,2,2)
    t_sam = 60:0.01:i;
    plot(t_sam,x_max(1:length(t_sam)))
    axis([60,120,0,1.2])
    xlabel("time/s")
    title("Figure 2: Mean-filted data")
    
    subplot(2,2,4)
    plot(60+0.01*[1:length(t_sam)],R_2(1:length(t_sam)),'-')
    hold on
    plot(60+0.01*timeset(find(timeset<(i-60)*100)),R_log(timeset(find(timeset<(i-60)*100))),'ro')
    for ii=1:length(timeset(find(timeset<(i-60)*100)))
        isodd = mod(ii,2);
        text(60+0.01*timeset(ii)+0.2,R_log(timeset(ii))+0.1,char(68*isodd+65*(1-isodd)),'fontsize',6);
    end
    ylabel('-log10(1-R)');
    xlabel('time/s');
    axis([60,120,0,4])
    title("Figure 3: Linear Recognization")
    
    subplot(2,2,3)
    node_alr = length(timeset(timeset<(i-60)*100));
    cycl_num = floor(node_alr/2);
    if cycl_num>=1
        if mod(node_alr,2)==0
            plot(t,x1(1:25600*i))
            xlabel("time/s")
            axis([timeset(node_alr)/100+60,timeset(node_alr+1)/100+59.2,-6,6])
            title(strcat('Figure 4: Life cycle #',num2str(cycl_num)))
        else
            plot(t,x1(1:25600*i))
            xlabel("time/s")
            axis([timeset(node_alr-1)/100+60,timeset(node_alr)/100+59.2,-6,6])
            title(strcat('Figure 4: Life cycle #',num2str(cycl_num)))
        end
    else
        xlabel("time/s")
        title('Figure 4: No life cycle')
    end
    picname=['pics/pf' num2str(i) '.png'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
    pause(0.5)
    close all
end

for i=121:240
    fprintf("%d\n",i);
    figure('color',[1 1 1])
    subplot(2,2,1)
    t=1/25600:1/25600:i;
    plot(t,x1(1:25600*i))
    xlabel("time/s")
    ylabel("Raw Data")
    axis([i-60,i,-6,6])
    title("Figure 1: Raw data")
    
    subplot(2,2,2)
    t_sam = 60:0.01:i;
    plot(t_sam,x_max(1:length(t_sam)))
    axis([i-60,i,0,1.2])
    xlabel("time/s")
    title("Figure 2: Mean-filted data")
    
    subplot(2,2,4)
    plot(60+0.01*[1:length(t_sam)],R_2(1:length(t_sam)),'-')
    hold on
    plot(60+0.01*timeset(find(timeset<(i-60)*100)),R_log(timeset(find(timeset<(i-60)*100))),'ro')
    for ii=1:length(timeset(find(timeset<(i-60)*100)))
        isodd = mod(ii,2);
        if 60+0.01*timeset(ii)>i-60
            text(60+0.01*timeset(ii)+0.2,R_log(timeset(ii))+0.1,char(68*isodd+65*(1-isodd)),'fontsize',6);
        end
    end
    ylabel('-log10(1-R)');
    xlabel('time/s');
    axis([i-60,i,0,4])
    title("Figure 3: Linear Recognization")
    
    subplot(2,2,3)
    node_alr = length(timeset(timeset<(i-60)*100));
    cycl_num = floor(node_alr/2);
    if cycl_num>=1
        if mod(node_alr,2)==0
            plot(t,x1(1:25600*i))
            xlabel("time/s")
            axis([timeset(node_alr)/100+60,timeset(node_alr+1)/100+59.2,-6,6])
            title(strcat('Figure 4: Life cycle #',num2str(cycl_num)))
        else
            plot(t,x1(1:25600*i))
            xlabel("time/s")
            axis([timeset(node_alr-1)/100+60,timeset(node_alr)/100+59.2,-6,6])
            title(strcat('Figure 4: Life cycle #',num2str(cycl_num)))
        end
    else
        xlabel("time/s")
        title('Figure 4: No life cycle')
    end
    picname=['pics/pf' num2str(i) '.png'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
    close all
end
