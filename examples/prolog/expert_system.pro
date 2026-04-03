% ═══════════════════════════════════════════════════════
% ANIMAL CLASSIFICATION EXPERT SYSTEM
% Identifies animals through hierarchical rules and
% demonstrates Prolog's logical inference capabilities
% ═══════════════════════════════════════════════════════

% ─── BASE CHARACTERISTICS ───
% Physical features of animals

has_feathers(eagle).
has_feathers(penguin).
has_feathers(sparrow).
has_feathers(parrot).
has_feathers(owl).
has_feathers(flamingo).

has_fur(dog).
has_fur(cat).
has_fur(bear).
has_fur(wolf).
has_fur(lion).
has_fur(tiger).
has_fur(rabbit).
has_fur(bat).

has_scales(snake).
has_scales(lizard).
has_scales(crocodile).
has_scales(turtle).
has_scales(salmon).
has_scales(shark).

% ─── REPRODUCTION ───

lays_eggs(eagle).
lays_eggs(penguin).
lays_eggs(sparrow).
lays_eggs(parrot).
lays_eggs(owl).
lays_eggs(flamingo).
lays_eggs(snake).
lays_eggs(lizard).
lays_eggs(crocodile).
lays_eggs(turtle).
lays_eggs(salmon).
lays_eggs(shark).

gives_birth(dog).
gives_birth(cat).
gives_birth(bear).
gives_birth(wolf).
gives_birth(lion).
gives_birth(tiger).
gives_birth(rabbit).
gives_birth(bat).

% ─── HABITAT ───

lives_in_water(penguin).
lives_in_water(salmon).
lives_in_water(shark).
lives_in_water(crocodile).
lives_in_water(turtle).

lives_on_land(dog).
lives_on_land(cat).
lives_on_land(bear).
lives_on_land(wolf).
lives_on_land(lion).
lives_on_land(tiger).
lives_on_land(rabbit).
lives_on_land(snake).
lives_on_land(lizard).
lives_on_land(eagle).
lives_on_land(sparrow).
lives_on_land(parrot).

can_fly(eagle).
can_fly(sparrow).
can_fly(parrot).
can_fly(owl).
can_fly(flamingo).
can_fly(bat).

% ─── DIET ───

eats_meat(eagle).
eats_meat(owl).
eats_meat(wolf).
eats_meat(lion).
eats_meat(tiger).
eats_meat(shark).
eats_meat(crocodile).
eats_meat(snake).
eats_meat(cat).

eats_plants(rabbit).
eats_plants(parrot).
eats_plants(flamingo).
eats_plants(turtle).
eats_plants(sparrow).

eats_both(dog).
eats_both(bear).
eats_both(lizard).

% ─── SIZE ───

size(eagle, large).
size(penguin, medium).
size(sparrow, small).
size(parrot, medium).
size(owl, medium).
size(flamingo, large).
size(dog, medium).
size(cat, small).
size(bear, large).
size(wolf, medium).
size(lion, large).
size(tiger, large).
size(rabbit, small).
size(bat, small).
size(snake, medium).
size(lizard, small).
size(crocodile, large).
size(turtle, medium).
size(salmon, medium).
size(shark, large).

% ─── CLASSIFICATION RULES ───

is_bird(X) :- has_feathers(X), lays_eggs(X).
is_mammal(X) :- has_fur(X), gives_birth(X).
is_reptile(X) :- has_scales(X), lays_eggs(X), lives_on_land(X).
is_fish(X) :- has_scales(X), lives_in_water(X), lays_eggs(X).
is_carnivore(X) :- eats_meat(X).
is_herbivore(X) :- eats_plants(X).
is_omnivore(X) :- eats_both(X).
is_predator(X) :- eats_meat(X), size(X, large).
is_prey(X) :- eats_plants(X), size(X, small).
is_flying_mammal(X) :- is_mammal(X), can_fly(X).
is_flightless_bird(X) :- is_bird(X), lives_in_water(X).
is_aquatic_reptile(X) :- has_scales(X), lives_in_water(X), lays_eggs(X).

% ─── DANGER ASSESSMENT ───

is_dangerous(X) :- is_predator(X).
is_dangerous(crocodile).
is_dangerous(shark).
is_dangerous(snake).

is_domestic(dog).
is_domestic(cat).
is_domestic(rabbit).
is_domestic(parrot).

is_safe(X) :- is_domestic(X).

% ═══════════════════════════════════════════════════════
% QUERIES - Test the expert system
% ═══════════════════════════════════════════════════════

% Query 1: Find all birds
?- is_bird(X).

% Query 2: Find all mammals
?- is_mammal(X).

% Query 3: Find all carnivores
?- is_carnivore(X).

% Query 4: Find all dangerous animals
?- is_dangerous(X).

% Query 5: Find all domestic/safe animals
?- is_safe(X).

% Query 6: Find large predators
?- is_predator(X).

% Query 7: Find prey animals
?- is_prey(X).

% Query 8: Verify specific classifications
?- is_bird(eagle).
?- is_mammal(dog).
?- is_reptile(snake).

% Query 9: Find flying mammals (bats!)
?- is_flying_mammal(X).

% Query 10: Find flightless birds
?- is_flightless_bird(X).

% Show the complete database
LISTING.
