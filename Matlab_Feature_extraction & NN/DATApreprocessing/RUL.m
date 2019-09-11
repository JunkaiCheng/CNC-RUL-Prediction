load('time.mat')
ourres = csvread('resultCsv1.csv',1,3);
ourres_int = interp1(time,ourres,[1:234])
%{
for i=1:30
    figure('color',[1 1 1])
    plot(1:i,234:-1:235-i,'-o',1:i,ourres_int(1:i),'-ro')
    axis([0,30,235-30,235])
    xlabel("# of Tools Produced")
    ylabel("RUL")
    l1 = legend("Theoretical RUL","Our Predicted RUL");
    set(l1,'Fontname', 'Times New Roman','FontWeight','bold','FontSize',12)
    picname=['pics/RUL' num2str(i) '.png'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
    close all
end
for i=31:234
    figure('color',[1 1 1])
    plot(1:234,234:-1:1,'-o',1:234,ourres_int,'-ro')
    axis([i-1,30+i-1,234-30-i+1,234-i+1])
    xlabel("# of Tools Produced")
    ylabel("RUL")
    l1 = legend("Theoretical RUL","Our Predicted RUL");
    set(l1,'Fontname', 'Times New Roman','FontWeight','bold','FontSize',12)
    picname=['pics/RUL' num2str(i) '.png'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
    close all
end
%}
for i=234-30+1:234
    figure('color',[1 1 1])
    plot(1:i,234:-1:235-i,'-o',1:i,ourres_int(1:i),'-ro')
    axis([234-30,234,0,30])
    xlabel("# of Tools Produced")
    ylabel("RUL")
    l1 = legend("Theoretical RUL","Our Predicted RUL");
    set(l1,'Fontname', 'Times New Roman','FontWeight','bold','FontSize',12)
    picname=['pics/RUL' num2str(i) '.png'];%保存的文件名：如i=1时，picname=1.fig
    saveas(gcf,picname)
    close all
end