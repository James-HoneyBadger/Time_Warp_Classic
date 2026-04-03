% ═══════════════════════════════════════════════════════
% WORLD GEOGRAPHY KNOWLEDGE BASE
% Comprehensive geographic facts and inferential rules
% for countries, capitals, continents, and relationships
% ═══════════════════════════════════════════════════════

% ─── CONTINENTS ───

continent(north_america).
continent(south_america).
continent(europe).
continent(asia).
continent(africa).
continent(oceania).
continent(antarctica).

% ─── COUNTRIES AND THEIR CONTINENTS ───

country(united_states, north_america).
country(canada, north_america).
country(mexico, north_america).
country(brazil, south_america).
country(argentina, south_america).
country(colombia, south_america).
country(united_kingdom, europe).
country(france, europe).
country(germany, europe).
country(italy, europe).
country(spain, europe).
country(japan, asia).
country(china, asia).
country(india, asia).
country(south_korea, asia).
country(australia, oceania).
country(new_zealand, oceania).
country(egypt, africa).
country(south_africa, africa).
country(nigeria, africa).
country(kenya, africa).

% ─── CAPITALS ───

capital(united_states, washington_dc).
capital(canada, ottawa).
capital(mexico, mexico_city).
capital(brazil, brasilia).
capital(argentina, buenos_aires).
capital(colombia, bogota).
capital(united_kingdom, london).
capital(france, paris).
capital(germany, berlin).
capital(italy, rome).
capital(spain, madrid).
capital(japan, tokyo).
capital(china, beijing).
capital(india, new_delhi).
capital(south_korea, seoul).
capital(australia, canberra).
capital(new_zealand, wellington).
capital(egypt, cairo).
capital(south_africa, pretoria).
capital(nigeria, abuja).
capital(kenya, nairobi).

% ─── POPULATION (approximate, millions) ───

population(united_states, 331).
population(canada, 38).
population(mexico, 129).
population(brazil, 214).
population(argentina, 46).
population(colombia, 51).
population(united_kingdom, 67).
population(france, 67).
population(germany, 83).
population(italy, 60).
population(spain, 47).
population(japan, 125).
population(china, 1412).
population(india, 1408).
population(south_korea, 52).
population(australia, 26).
population(new_zealand, 5).
population(egypt, 104).
population(south_africa, 60).
population(nigeria, 218).
population(kenya, 55).

% ─── LANGUAGES ───

speaks(united_states, english).
speaks(canada, english).
speaks(canada, french).
speaks(mexico, spanish).
speaks(brazil, portuguese).
speaks(argentina, spanish).
speaks(colombia, spanish).
speaks(united_kingdom, english).
speaks(france, french).
speaks(germany, german).
speaks(italy, italian).
speaks(spain, spanish).
speaks(japan, japanese).
speaks(china, mandarin).
speaks(india, hindi).
speaks(india, english).
speaks(south_korea, korean).
speaks(australia, english).
speaks(new_zealand, english).
speaks(egypt, arabic).
speaks(south_africa, english).
speaks(nigeria, english).
speaks(kenya, english).
speaks(kenya, swahili).

% ─── CURRENCIES ───

currency(united_states, dollar).
currency(canada, dollar).
currency(united_kingdom, pound).
currency(japan, yen).
currency(china, yuan).
currency(india, rupee).
currency(australia, dollar).
currency(brazil, real).
currency(mexico, peso).
currency(south_korea, won).
currency(france, euro).
currency(germany, euro).
currency(italy, euro).
currency(spain, euro).

% ─── INFERENCE RULES ───

% Two countries are neighbors if on the same continent
same_continent(X, Y) :- country(X, C), country(Y, C).

% A country is large if population > 100 million
is_large_country(X) :- population(X, P), P > 100.

% A country is small if population < 50 million
is_small_country(X) :- population(X, P), P < 50.

% Countries sharing a language
shares_language(X, Y) :- speaks(X, L), speaks(Y, L).

% European Union members (simplified)
eu_member(france).
eu_member(germany).
eu_member(italy).
eu_member(spain).
is_eu_country(X) :- eu_member(X).

% English-speaking countries
english_speaking(X) :- speaks(X, english).

% Countries using the euro
uses_euro(X) :- currency(X, euro).

% Countries using the dollar (any variant)
uses_dollar(X) :- currency(X, dollar).

% ═══════════════════════════════════════════════════════
% QUERIES - Explore the knowledge base
% ═══════════════════════════════════════════════════════

% Query 1: Find all European countries
?- country(X, europe).

% Query 2: Find all capitals
?- capital(X, Y).

% Query 3: Find large countries (>100M population)
?- is_large_country(X).

% Query 4: Find all English-speaking countries
?- english_speaking(X).

% Query 5: Find countries that use the euro
?- uses_euro(X).

% Query 6: Find countries on the same continent as Japan
?- same_continent(japan, X).

% Query 7: What language does Brazil speak?
?- speaks(brazil, X).

% Query 8: What is the capital of France?
?- capital(france, X).

% Query 9: Find all African countries
?- country(X, africa).

% Query 10: Find countries sharing a language with India
?- shares_language(india, X).

% Show complete database
LISTING.
