
syms t
A = symmatrix('A',[L 3])

Ap1 = circshift(A, 1,1);
Am1 = circshift(A,-1,1);

E = symmatrix2sym(symmatcross(Ap1-Am1,Ap1+Am1-2*A));

ODE = matlabFunction(E(:),'Vars',{t,symmatrix2sym(A)})

GE = [];
for s=1:L
for t=(s+1):L
s:t
end
end