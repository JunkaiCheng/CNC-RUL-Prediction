clear all
clc
F=[1 2 3 4 5 6 7 8];
N=8;
L=6;

FF=wgn(N,1,-10)+5*sin(2*pi*0.003.*[1:N]');

for i=1:L
    for j=1:N-L+1
        X(i,j)=F(i+j-1);
    end
end
X

S=X*X'
[V,D]=eig(S); %
[d,ind] = sort(diag(D));
d=flipud(d);
ind=flipud(ind);
Ds = D(ind,ind)
Vs = V(:,ind)
S*Vs(:,1)-Ds(1,1)*Vs(:,1); %should be 0, Av=\lam v.