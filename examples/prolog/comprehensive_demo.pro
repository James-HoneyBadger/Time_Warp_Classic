% =========================================================
% COMPREHENSIVE PROLOG DEMO - Time Warp Classic IDE
% Demonstrates all major Prolog language features
% =========================================================

% --- FACTS ---
% Parent relationships
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

% Animal facts
animal(dog).
animal(cat).
animal(bird).
animal(fish).

% Color facts
color(red).
color(blue).
color(green).
color(yellow).

% Number facts
number(1).
number(2).
number(3).
number(4).
number(5).

% --- RULES ---
% Grandparent rule
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

% Ancestor rule
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% Sibling rule
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% List operations
list_length([], 0).
list_length([_|T], N) :- list_length(T, N1), N is N1 + 1.

append([], L, L).
append([H|T1], L2, [H|T3]) :- append(T1, L2, T3).

member(X, [X|_]).
member(X, [_|T]) :- member(X, T).

% Sum list elements
sum_list([], 0).
sum_list([H|T], Sum) :- sum_list(T, RestSum), Sum is H + RestSum.

% Maximum of a list
max_list([X], X).
max_list([H|T], Max) :- max_list(T, MaxT), (H > MaxT -> Max = H; Max = MaxT).

% Factorial
factorial(0, 1).
factorial(N, F) :- N > 0, N1 is N - 1, factorial(N1, F1), F is N * F1.

% Check even/odd
even(X) :- 0 is X mod 2.
odd(X) :- 1 is X mod 2.

% Check prime
is_prime(2).
is_prime(3).
is_prime(N) :- N > 3, N mod 2 =\= 0, not_divisible(N, 3).

not_divisible(N, D) :- D * D > N, !.
not_divisible(N, D) :- N mod D =\= 0, D2 is D + 2, not_divisible(N, D2).

% --- MAIN QUERY DEMONSTRATION ---
:- write('=================================================='), nl.
:- write('COMPREHENSIVE PROLOG DEMO'), nl.
:- write('=================================================='), nl, nl.

% --- Facts demonstration
:- write('=== FACTS ==='), nl.
:- write('Animals:'), nl, forall(animal(X), (write('  '), write(X), nl)).
:- write('Colors:'), nl, forall(color(X), (write('  '), write(X), nl)).
:- nl.

% --- Parent-child relationships
:- write('=== PARENT-CHILD RELATIONSHIPS ==='), nl.
:- forall(parent(X, Y), (write('  '), write(X), write(' is parent of '), write(Y), nl)).
:- nl.

% --- Grandparent relationships
:- write('=== GRANDPARENT RELATIONSHIPS ==='), nl.
:- forall(grandparent(X, Y), (write('  '), write(X), write(' is grandparent of '), write(Y), nl)).
:- nl.

% --- Sibling relationships
:- write('=== SIBLING RELATIONSHIPS ==='), nl.
:- forall(sibling(X, Y), (write('  '), write(X), write(' is sibling of '), write(Y), nl)).
:- nl.

% --- Ancestor relationships
:- write('=== ANCESTOR RELATIONSHIPS ==='), nl.
:- forall(ancestor(X, Y), (write('  '), write(X), write(' is ancestor of '), write(Y), nl)).
:- nl.

% --- List operations
:- write('=== LIST OPERATIONS ==='), nl.
:- append([1, 2], [3, 4], L1), write('append([1,2], [3,4], L): L = '), write(L1), nl.
:- list_length([a, b, c, d], Len), write('length([a,b,c,d]): '), write(Len), nl.
:- member(3, [1, 2, 3, 4]), write('member(3, [1,2,3,4]): true'), nl.
:- sum_list([1, 2, 3, 4, 5], Sum), write('sum([1,2,3,4,5]): '), write(Sum), nl.
:- max_list([3, 7, 2, 9, 1], Max), write('max([3,7,2,9,1]): '), write(Max), nl.
:- nl.

% --- Arithmetic operations
:- write('=== ARITHMETIC OPERATIONS ==='), nl.
:- X is 10 + 5, write('10 + 5 = '), write(X), nl.
:- Y is 10 - 3, write('10 - 3 = '), write(Y), nl.
:- Z is 4 * 5, write('4 * 5 = '), write(Z), nl.
:- W is 20 / 4, write('20 / 4 = '), write(W), nl.
:- M is 17 mod 5, write('17 mod 5 = '), write(M), nl.
:- nl.

% --- Comparison operations
:- write('=== COMPARISON OPERATIONS ==='), nl.
:- (5 > 3 -> write('5 > 3: true') ; write('5 > 3: false')), nl.
:- (5 = 5 -> write('5 = 5: true') ; write('5 = 5: false')), nl.
:- (5 < 10 -> write('5 < 10: true') ; write('5 < 10: false')), nl.
:- (5 =:= 5 -> write('5 =:= 5: true') ; write('5 =:= 5: false')), nl.
:- (5 =\= 3 -> write('5 =\\= 3: true') ; write('5 =\\= 3: false')), nl.
:- nl.

% --- Factorial calculation
:- write('=== FACTORIAL CALCULATION ==='), nl.
:- factorial(5, F5), write('factorial(5) = '), write(F5), nl.
:- factorial(6, F6), write('factorial(6) = '), write(F6), nl.
:- nl.

% --- Number properties
:- write('=== NUMBER PROPERTIES ==='), nl.
:- (even(4) -> write('4 is even') ; write('4 is odd')), nl.
:- (odd(5) -> write('5 is odd') ; write('5 is even')), nl.
:- (even(6) -> write('6 is even') ; write('6 is odd')), nl.
:- nl.

% --- Prime checking
:- write('=== PRIME NUMBERS ==='), nl.
:- (is_prime(2) -> write('2 is prime') ; write('2 is not prime')), nl.
:- (is_prime(5) -> write('5 is prime') ; write('5 is not prime')), nl.
:- (is_prime(11) -> write('11 is prime') ; write('11 is not prime')), nl.
:- (is_prime(12) -> write('12 is prime') ; write('12 is not prime')), nl.
:- nl.

% --- Unification examples
:- write('=== UNIFICATION ==='), nl.
:- X = Y, Y = 42, write('X = Y, Y = 42: X = '), write(X), nl.
:- [H|T] = [1, 2, 3], write('[H|T] = [1,2,3]: H = '), write(H), write(', T = '), write(T), nl.
:- nl.

% --- Logical operations
:- write('=== LOGICAL OPERATIONS ==='), nl.
:- ((5 > 3, 10 > 5) -> write('AND (5>3, 10>5): true') ; write('AND: false')), nl.
:- ((5 > 3 ; 10 < 5) -> write('OR (5>3 ; 10<5): true') ; write('OR: false')), nl.
:- ((not (5 < 3)) -> write('NOT (not 5<3): true') ; write('NOT: false')), nl.
:- nl.

% --- Backtracking example
:- write('=== BACKTRACKING ==='), nl.
:- write('All animals: '), findall(A, animal(A), Animals), write(Animals), nl.
:- write('All colors: '), findall(C, color(C), Colors), write(Colors), nl.
:- nl.

% --- Final message
:- write('=================================================='), nl.
:- write('PROLOG DEMO COMPLETE!'), nl.
:- write('All major Prolog features demonstrated!'), nl.
:- write('=================================================='), nl.
