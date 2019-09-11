figure('color',[1 1 1])
for i=60:120
    t=1/25600:1/25600:i;
    plot(t,x1(1:25600*i))
    xlabel("time/s")
    ylabel("Raw Data")
    axis([60,120,-6,6])
    pause(0.05)
    picname=['pics/' num2str(i) '.fig'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
end
for i=121:240
    t=i-60:1/25600:i;
    plot(t,x1(25600*(i-60):25600*i))
    xlabel("time/s")
    ylabel("Raw Data")
    axis([i-60,i,-6,6])
    pause(0.05)
    picname=['pics/' num2str(i) '.fig'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
end