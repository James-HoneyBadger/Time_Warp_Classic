# Prolog Language Reference

Complete reference for Prolog syntax in Time Warp Classic.

## Logic Programming Basics

Prolog is a logic programming language based on:
1. **Facts** - Statements that are true
2. **Rules** - How to derive new facts
3. **Queries** - Questions to ask

## Facts

```prolog
% Facts about people
parent(tom, bob).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

% Facts about likes
likes(mary, wine).
likes(john, wine).
likes(john, mary).
```

## Rules

```prolog
% grandfather(X, Z) is true if X is parent of Y and Y is parent of Z
grandfather(X, Z) :- parent(X, Y), parent(Y, Z).

% ancestor(X, Y) is true if X is parent of Y or ancestor of parent of Y
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).

% sibling(X, Y) if they have the same parent
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.
```

## Queries

```prolog
% Query: Is tom a parent of bob?
?- parent(tom, bob).
% Result: yes

% Query: Who is a parent of bob?
?- parent(X, bob).
% Result: X = tom

% Query: Who are bob's children?
?- parent(bob, X).
% Result: X = ann ; X = pat

% Query: Who is a grandparent of jim?
?- grandfather(X, jim).
% Result: X = bob
```

## Built-in Predicates

### Arithmetic Comparison

```prolog
X > Y       % Greater than
X < Y       % Less than
X >= Y      % Greater or equal
X =< Y      % Less or equal
X =:= Y     % Equal value
X =\= Y     % Not equal value
```

### Type Testing

```prolog
atom(X)         % Is X an atom?
number(X)       % Is X a number?
integer(X)      % Is X an integer?
compound(X)     % Is X a compound term?
var(X)          % Is X an unbound variable?
nonvar(X)       % Is X not a variable?
```

### List Operations

```prolog
append([1,2], [3,4], X).    % X = [1,2,3,4]
length([a,b,c], N).         % N = 3
member(X, [a,b,c]).         % X = a ; b ; c
reverse([1,2,3], X).        % X = [3,2,1]
```

### List Processing

```prolog
% List syntax: [Head | Tail]
[H|T] = [1,2,3].
% H = 1, T = [2,3]

% Check if member
member(X, [H|T]) :- X = H.
member(X, [_|T]) :- member(X, T).

% Sum list
sum_list([], 0).
sum_list([H|T], Sum) :- sum_list(T, RestSum), Sum is H + RestSum.
```

## Arithmetic

### Is Operator

```prolog
?- X is 2 + 3.
% X = 5

?- X is 10 / 2.
% X = 5.0

?- X is 2 ** 3.
% X = 8

?- X is 7 mod 3.
% X = 1
```

### Math Functions

```prolog
is abs(-5), 5.          % Absolute value
is sqrt(16), 4.         % Square root
is sin(0), 0.           % Sine
is max(5, 3), 5.        % Maximum
is min(5, 3), 3.        % Minimum
```

## Control Structures

### Cut (!)

```prolog
max(X, Y, X) :- X >= Y, !.
max(X, Y, Y).

% This ensures only first matching clause is used
```

### If-Then-Else

```prolog
(condition -> action1 ; action2)

?- (5 > 3 -> write('yes') ; write('no')).
% Output: yes
```

### Negation

```prolog
\+ member(X, [1,2,3]).      % X is not in list

not_in_list(X, List) :- \+ member(X, List).
```

## List Predicates

### Common List Operations

```prolog
% Get element at index (1-based)
nth1(1, [a,b,c], X).        % X = a

% Get all elements satisfying condition
findall(X, parent(tom, X), Children).

% Test all elements satisfy condition
forall(member(X, [1,2,3]), X > 0).

% Select element from list
select(X, [a,b,c], Rest).
```

## Facts Database

### Assert (Add Facts)

```prolog
:- assert(parent(john, mary)).
:- assertz(likes(john, pizza)).   % Add at end
:- asserta(likes(john, pizza)).   % Add at beginning
```

### Retract (Remove Facts)

```prolog
:- retract(parent(john, mary)).
:- retractall(parent(john, _)).  % Remove all matching
```

## Complete Examples

### Family Relationships

```prolog
% Facts
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
parent(pat, jim).

% Rules
grandparent(X, Y) :- parent(X, Z), parent(Z, Y).
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

% Queries
?- parent(tom, X).         % Who are tom's children?
?- grandparent(tom, X).    % Who are tom's grandchildren?
?- ancestor(tom, X).       % Who are tom's descendants?
?- sibling(bob, X).        % Who is bob's sibling?
```

### List Processing

```prolog
% Sum of list
sum_list([], 0).
sum_list([H|T], Sum) :-
    sum_list(T, RestSum),
    Sum is H + RestSum.

% Maximum of list
max_list([X], X).
max_list([H|T], Max) :-
    max_list(T, MaxT),
    (H > MaxT -> Max = H ; Max = MaxT).

?- sum_list([1,2,3,4,5], Sum).       % Sum = 15
?- max_list([3,1,4,1,5], Max).       % Max = 5
```

### Number Guessing Game

```prolog
guess_number :-
    Secret = 42,
    repeat,
    write('Guess a number: '),
    read(Guess),
    (Guess =:= Secret ->
        write('Correct!'), nl
    ; Guess > Secret ->
        write('Too high'), nl, fail
    ;
        write('Too low'), nl, fail
    ).
```

## Debugging

### Trace Execution

```prolog
?- trace.               % Enable tracing
?- parent(tom, X).      % Execute with trace
?- notrace.             % Disable tracing
```

### Check Predicates

```prolog
?- current_predicate(parent/2).    % Does predicate exist?
?- listing(parent).                % Show definition
```

## Tips & Best Practices

1. **Use descriptive names** for facts and rules
2. **Order clauses carefully** (more specific first)
3. **Use cut (!) wisely** to prevent backtracking
4. **List recursion** is natural in Prolog
5. **Test incrementally** with small examples
6. **Use write/1 for debugging** facts

## Common Patterns

### Recursion Pattern
```prolog
process([], []).
process([H|T], [ProcessedH|ProcessedT]) :-
    process_element(H, ProcessedH),
    process(T, ProcessedT).
```

### Accumulator Pattern
```prolog
sum_list(List, Sum) :- sum_list(List, 0, Sum).
sum_list([], Acc, Acc).
sum_list([H|T], Acc, Sum) :-
    NewAcc is Acc + H,
    sum_list(T, NewAcc, Sum).
```

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/prolog/](../../examples/prolog/)

---

**Last Updated:** 2024
