syms x1_2 x2_2 x3_2 x4_2 u1_2 u2_2 v2;
syms x1_1 x2_1 x3_1 x4_1 u1_1 u2_1 v1;
syms x1_0 x2_0 x3_0 x4_0 u1_0 u2_0 v0;
g = 10;%�������ٶȣ�ˮƽ������ٶ�=g*u2,u2�˴���ʾpitch��
tp = 0.1;%ʱ�䲽��Ϊ0.1s
lam1 = 0.1;
lam2 = 10;
% v(3) = 0;
v2 = lam1*(x1_2 - 3)^2 + lam2*(x3_2 + x1_2*u2_2 - 1)^2;
u2_2 = solve(0 == diff(v2,u2_2),u2_2);
v2 = subs(v2);

% position iteration
% k = 1ʱ�̵�����ʽ
% x2_1 = x2_0 + g*u2_1;   % k=1ʱ���ٶȵ�����ʽ x2(1) = x2(0) + g*u2(1)  ��ʽ������ k=0
% ʱ�̵�ֵx2(0),�������ǻ�û�Ƶ�0ʱ���ء�
x1_2 = x1_1 + x2_1*tp + 0.5*g*u2_1*tp;% k=1ʱ��λ�õ�����ʽ�� x1(2) = x1(1) + x2(1) + 0.5*g*u2(1)
% update param with tp
% x1_2 = subs(x1_2);
% no velocity iteration
v1 = subs(v2) + lam1*(x1_1 - 3)^2 + lam2*(x3_1 + x1_1*u2_1 - 1)^2;
u2_1 = solve(0 == diff(v1,u2_1),u2_1);
v1 = subs(v1);

% position iteration
x1_1 = x1_0 + x2_0*tp + 0.5*g*u2_0*tp;
x3_1 = x3_0 + x4_0*tp + 0.5*u1_0*tp;
% velocity iteration
x2_1 = x2_0 + g*u2_0*tp;
% update param with tp
% x1_1 = subs(x1_1);
% x3_1 = subs(x3_1);
% x2_1 = subs(x2_1);


v0 = subs(v1) + lam1*(x1_0 - 3)^2 + lam2*(x3_0 + x1_0*u2_0 - 1)^2;
eqns_0 = [0 == diff(v0,u1_0),0 == diff(v0,u2_0)];
vars_0 = [u1_0, u2_0];
[u1_0,u2_0] = solve(eqns_0,vars_0);
v0 = subs(v0);

% syms a b c d x1 x2;
% eqns = [0==a*x1+b*x2,1==c*x1+d*x2];
% vars = [x1,x2];
% [x1,x2] = solve(eqns,vars);
