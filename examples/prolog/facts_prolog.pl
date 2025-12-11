% ====================================
%    Prolog Demo - Logic Programming
% ====================================

% Facts about programming languages
created(basic, 1964).
created(logo, 1967).
created(pascal, 1970).
created(prolog, 1972).
created(forth, 1970).

paradigm(basic, imperative).
paradigm(logo, educational).
paradigm(pascal, structured).
paradigm(prolog, logic).
paradigm(forth, stack).

creator(basic, 'John Kemeny and Thomas Kurtz').
creator(logo, 'Wally Feurzeig and Seymour Papert').
creator(pascal, 'Niklaus Wirth').
creator(prolog, 'Alain Colmerauer').
creator(forth, 'Charles Moore').

% Rules
is_vintage(Language) :- created(Language, Year), Year < 1980.
uses_logic(Language) :- paradigm(Language, logic).

% Family relationships for demonstration
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% Sample queries (these would be run at the prompt):
% ?- created(prolog, Year).
% ?- is_vintage(X).
% ?- grandparent(tom, Who).
% ?- ancestor(tom, jim).

% Print welcome message
:- write('Welcome to Time Warp Prolog!'), nl,
   write('Prolog is a logic programming language.'), nl,
   write('Try querying: created(prolog, Year).'), nl.
