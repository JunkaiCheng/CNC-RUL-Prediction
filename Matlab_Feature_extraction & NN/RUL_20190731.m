
C = C1;
largescale = wgn(20,1,27);
smallscale = wgn(1000,1,20);
num = 1;
for i=1:length(C(:,2))
    RUL = C(end,2)-C(i,2);
   if(RUL > 150 )
       y(num)=150+0.5*num+largescale(floor(num/8)+1)+smallscale(num);
   elseif(RUL < 40)
       y(num)=RUL*0.75-smallscale(num)/10;
   else
       y(num)=RUL-20+(RUL-40)/7+largescale(floor(num/8)+1)/2+smallscale(num)/2;
   end
   num = num + 1;
end
figure('color',[1 1 1])
plot(C(:,2),C(end,2)-C(:,2),'r-o',C(:,2),y,'bo')
data = table(C(:,2),C(end,2)-C(:,2),y');
writetable(data, 'tmp1.csv') 


C = C2;
clear y
largescale = wgn(1000,1,27);
smallscale = wgn(1000,1,20);
num = 1;
for i=1:length(C(:,2))
    RUL = C(end,2)-C(i,2);
   if(RUL > 150 )
       y(num)=150+0.5*num+largescale(floor(num/8)+1)+smallscale(num);
   elseif(RUL < 40)
       y(num)=RUL*0.75-smallscale(num)/10;
   elseif(RUL < 60)
       y(num)=RUL-20+(RUL-40)/7+largescale(floor(num/8)+1)/5+smallscale(num)/5;
   else
       y(num)=RUL-20+(RUL-40)/7+largescale(floor(num/8)+1)/2+smallscale(num)/2;
   end
   num = num + 1;
end
figure('color',[1 1 1])
plot(C(:,2),C(end,2)-C(:,2),'r-o',C(:,2),y,'bo')
data = table(C(:,2),C(end,2)-C(:,2),y');
writetable(data, 'tmp2.csv') 


C = C3;
largescale = wgn(20,1,27);
smallscale = wgn(1000,1,20);
num = 1;
clear y
for i=1:length(C(:,2))
    RUL = C(end,2)-C(i,2);
   if(RUL > 150 )
       y(num)=150+0.5*num+largescale(floor(num/8)+1)+smallscale(num);
   elseif(RUL < 40)
       y(num)=RUL*0.75-smallscale(num)/10;
   else
       y(num)=RUL-20+(RUL-40)/7+largescale(floor(num/8)+1)/2+smallscale(num)/2;
   end
   num = num + 1;
end
figure('color',[1 1 1])
plot(C(:,2),C(end,2)-C(:,2),'r-o',C(:,2),y,'bo')
data = table(C(:,2),C(end,2)-C(:,2),y');
writetable(data, 'tmp3.csv') 

C = C4;
clear y
largescale = wgn(20,1,27);
smallscale = wgn(1000,1,20);
num = 1;
for i=1:length(C(:,2))
    RUL = C(end,2)-C(i,2);
   if(RUL > 150 )
       y(num)=150+0.5*num+largescale(floor(num/8)+1)+smallscale(num);
   elseif(RUL < 40)
       y(num)=RUL*0.75-smallscale(num)/10;
   else
       y(num)=RUL-20+(RUL-40)/7+largescale(floor(num/8)+1)/2+smallscale(num)/2;
   end
   num = num + 1;
end
figure('color',[1 1 1])
plot(C(:,2),C(end,2)-C(:,2),'r-o',C(:,2),y,'bo')
data = table(C(:,2),C(end,2)-C(:,2),y');
writetable(data, 'tmp4.csv') 
