#const n = 6.
#const m = 5.
#const k = 3.

char(a).
char(b).
char(c).
char(d).
char(e).

s(0, 0, a).
s(0, 1, b).
s(0, 2, c).
s(0, 3, d).
s(0, 4, e).

s(1, 0, a).
s(1, 1, a).
s(1, 2, a).
s(1, 3, a).
s(1, 4, a).

s(2, 0, b).
s(2, 1, b).
s(2, 2, b).
s(2, 3, b).
s(2, 4, b).

s(3, 0, c).
s(3, 1, c).
s(3, 2, c).
s(3, 3, c).
s(3, 4, c).

s(4, 0, d).
s(4, 1, d).
s(4, 2, d).
s(4, 3, e).
s(4, 4, e).

s(5, 0, a).
s(5, 1, a).
s(5, 2, c).
s(5, 3, c).
s(5, 4, e).

word(0..n-1).
site(0..m-1).

1 {x(I) : word(I)} n.
{y(J) : site(J)} = m-k.
{z(J, A) : char(A)} = 1 :- site(J).
m-k {yz(J, A) : s(I, J, A)} :- x(I).
:- y(J), z(J, A), not yz(J, A).
:- yz(J, A), not y(J).
:- yz(J, A), y(J), not z(J, A).
#maximize{1, I : x(I)}.
