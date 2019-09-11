t1 = 2792;
t2 = 3379;
s1 = (60+0.01*(t1-1))*25600;
s2 = (60+0.01*(t2-1))*25600;
x1_sam = x1(s1:s2);
plot(x1(s1:s2))
Y = fft(x1_sam, s2-s1);
N=s2-s1;
Ayy = abs(Y);
figure;
Ayy = Ayy/(N/2);
F = ([1:N]-1)*25600/N;
figure('color',[1 1 1])
plot(F(1:N/2),20*log10(Ayy(1:N/2)))
axis([-inf,inf,-40,10])
xlabel("Frequency(Hz)");
ylabel("Power(dB)")