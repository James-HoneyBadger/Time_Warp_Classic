% Prolog Logic Programming Demo
% Demonstrates facts, rules, and queries

% Facts about family relationships
parent(alice, bob).
parent(alice, charlie).
parent(bob, david).
parent(bob, eve).
parent(charlie, frank).

% Gender facts
male(bob).
male(charlie).
male(david).
male(frank).
female(alice).
female(eve).

% Rules defining relationships
father(X, Y) :- parent(X, Y), male(X).
mother(X, Y) :- parent(X, Y), female(X).

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
grandfather(X, Z) :- grandparent(X, Z), male(X).
grandmother(X, Z) :- grandparent(X, Z), female(X).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% Rules for ancestors
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% Demo queries (these would be run interactively)
% ?- father(bob, david).        % Should return true
% ?- mother(alice, bob).        % Should return true
% ?- grandparent(alice, david). % Should return true
% ?- sibling(bob, charlie).     % Should return true
% ?- ancestor(alice, frank).    % Should return true

% Additional demo facts
likes(alice, reading).
likes(bob, programming).
likes(charlie, music).
likes(david, games).

% Rules for interests
shares_interest(X, Y) :- likes(X, Z), likes(Y, Z), X \= Y.

% Demo program that shows some results
demo :-
    write('Prolog Logic Programming Demo'), nl,
    write('==============================='), nl, nl,

    write('Family relationships:'), nl,
    (father(F, C) -> write(F), write(' is father of '), write(C), nl ; true),
    fail.
demo :-
    nl,
    write('Grandparent relationships:'), nl,
    (grandparent(GP, GC) -> write(GP), write(' is grandparent of '), write(GC), nl ; true),
    fail.
demo :-
    nl,
    write('Shared interests:'), nl,
    (shares_interest(P1, P2) -> write(P1), write(' and '), write(P2), write(' share interests'), nl ; true),
    fail.
demo :-
    nl,
    write('Demo complete!'), nl.

% Run demo when file is loaded
:- demo.