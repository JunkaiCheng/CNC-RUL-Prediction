%{
clear;
Fs=1000;
n=0:1/Fs:1;
xn = wgn(1,Fs+1,20);
nfft = 1024;
window2 = blackman(100);
noverlap = 20;
range = 'onesided';
[Pxx2,f]=pwelch(xn,window2,noverlap,nfft,Fs,range);
plot_Pxx2 = 10*log10(Pxx2);
figure(3)
plot(f,plot_Pxx2)
%}
clear all
n = 0:1:319;
x = sinc(0.2*n);
[pxx,w] = periodogram(x);
plot(w,10*log10(pxx))