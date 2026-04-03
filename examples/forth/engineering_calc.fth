\ ═══════════════════════════════════════════════════════
\ ENGINEERING UNIT CONVERTER
\ A practical unit conversion suite using Forth's
\ stack-based computation for engineering calculations
\ ═══════════════════════════════════════════════════════

: HEADER ." ═══════════════════════════════════════════" CR ;
: DIVIDER ."  ─────────────────────────────────────────" CR ;

HEADER
."  ENGINEERING UNIT CONVERTER v1.0" CR
HEADER
CR

\ ═══════════════════════════════════════
\ TEMPERATURE CONVERSIONS
\ ═══════════════════════════════════════

: C-TO-F  ( c -- f )  9 * 5 / 32 + ;
: F-TO-C  ( f -- c )  32 - 5 * 9 / ;
: C-TO-K  ( c -- k )  273 + ;
: K-TO-C  ( k -- c )  273 - ;

."  TEMPERATURE CONVERSIONS" CR
DIVIDER

."   Celsius → Fahrenheit:" CR
0 DUP . ."  °C = " C-TO-F . ."  °F" CR
20 DUP . ."  °C = " C-TO-F . ."  °F" CR
37 DUP . ."  °C = " C-TO-F . ."  °F (body temp)" CR
100 DUP . ."  °C = " C-TO-F . ."  °F (boiling)" CR
CR

."   Fahrenheit → Celsius:" CR
32 DUP . ."  °F = " F-TO-C . ."  °C (freezing)" CR
72 DUP . ."  °F = " F-TO-C . ."  °C (room temp)" CR
212 DUP . ."  °F = " F-TO-C . ."  °C (boiling)" CR
CR

."   Celsius → Kelvin:" CR
0 DUP . ."  °C = " C-TO-K . ."  K" CR
25 DUP . ."  °C = " C-TO-K . ."  K" CR
100 DUP . ."  °C = " C-TO-K . ."  K" CR
CR

\ ═══════════════════════════════════════
\ DISTANCE CONVERSIONS
\ ═══════════════════════════════════════

: MI-TO-KM   ( mi -- km )  161 * 100 / ;
: KM-TO-MI   ( km -- mi )  100 * 161 / ;
: FT-TO-M    ( ft -- m*100 )  3048 * 10000 / ;
: IN-TO-CM   ( in -- cm*10 )  254 * 100 / ;

."  DISTANCE CONVERSIONS" CR
DIVIDER

."   Miles → Kilometers:" CR
1 DUP . ."  mi = " MI-TO-KM . ."  km" CR
5 DUP . ."  mi = " MI-TO-KM . ."  km" CR
26 DUP . ."  mi (marathon) = " MI-TO-KM . ."  km" CR
100 DUP . ."  mi = " MI-TO-KM . ."  km" CR
CR

."   Kilometers → Miles:" CR
1 DUP . ."  km = " KM-TO-MI . ."  mi" CR
10 DUP . ."  km = " KM-TO-MI . ."  mi" CR
42 DUP . ."  km (marathon) = " KM-TO-MI . ."  mi" CR
CR

\ ═══════════════════════════════════════
\ WEIGHT CONVERSIONS
\ ═══════════════════════════════════════

: LB-TO-KG   ( lb*10 -- kg*10 )  4536 * 10000 / ;
: KG-TO-LB   ( kg -- lb*10 )  2205 * 100 / ;
: OZ-TO-G    ( oz -- g )  28 * ;

."  WEIGHT CONVERSIONS" CR
DIVIDER

."   Pounds → Kilograms (approx):" CR
10 DUP . ."  lb ≈ " LB-TO-KG . ."  kg" CR
50 DUP . ."  lb ≈ " LB-TO-KG . ."  kg" CR
150 DUP . ."  lb ≈ " LB-TO-KG . ."  kg" CR
200 DUP . ."  lb ≈ " LB-TO-KG . ."  kg" CR
CR

."   Kilograms → Pounds (x10):" CR
1 DUP . ."  kg ≈ " KG-TO-LB . ."  (x10 lb)" CR
50 DUP . ."  kg ≈ " KG-TO-LB . ."  (x10 lb)" CR
100 DUP . ."  kg ≈ " KG-TO-LB . ."  (x10 lb)" CR
CR

."   Ounces → Grams:" CR
1 DUP . ."  oz = " OZ-TO-G . ."  g" CR
8 DUP . ."  oz = " OZ-TO-G . ."  g" CR
16 DUP . ."  oz (1 lb) = " OZ-TO-G . ."  g" CR
CR

\ ═══════════════════════════════════════
\ AREA CONVERSIONS
\ ═══════════════════════════════════════

: SQFT-TO-SQM  ( sqft -- sqm*10 )  929 * 10000 / ;
: ACRES-TO-HA  ( acres*10 -- ha*10 )  4047 * 10000 / ;

."  AREA CONVERSIONS" CR
DIVIDER

."   Sq Feet → Sq Meters (approx):" CR
100 DUP . ."  sq ft ≈ " SQFT-TO-SQM . ."  sq m" CR
500 DUP . ."  sq ft ≈ " SQFT-TO-SQM . ."  sq m" CR
1000 DUP . ."  sq ft ≈ " SQFT-TO-SQM . ."  sq m" CR
2000 DUP . ."  sq ft ≈ " SQFT-TO-SQM . ."  sq m" CR
CR

\ ═══════════════════════════════════════
\ ELECTRICAL ENGINEERING
\ ═══════════════════════════════════════

: OHM-V  ( i r -- v )  * ;
: OHM-I  ( v r -- i )  / ;
: OHM-R  ( v i -- r )  / ;
: POWER  ( v i -- p )  * ;

."  ELECTRICAL ENGINEERING (OHM'S LAW)" CR
DIVIDER

."   V = I × R (Voltage):" CR
."   2A through 100Ω: V = " 2 100 OHM-V . ."  volts" CR
."   5A through 20Ω:  V = " 5 20 OHM-V . ."  volts" CR
CR

."   I = V / R (Current):" CR
."   12V across 4Ω:   I = " 12 4 OHM-I . ."  amps" CR
."   120V across 60Ω: I = " 120 60 OHM-I . ."  amps" CR
CR

."   R = V / I (Resistance):" CR
."   24V at 3A:       R = " 24 3 OHM-R . ."  ohms" CR
."   120V at 10A:     R = " 120 10 OHM-R . ."  ohms" CR
CR

."   P = V × I (Power):" CR
."   120V at 10A:     P = " 120 10 POWER . ."  watts" CR
."   240V at 30A:     P = " 240 30 POWER . ."  watts" CR
CR

\ ═══════════════════════════════════════
\ RESISTOR COMBINATIONS
\ ═══════════════════════════════════════

: R-SERIES  ( r1 r2 -- r_total )  + ;

."  RESISTOR COMBINATIONS" CR
DIVIDER

."   Series: R1 + R2:" CR
."   100Ω + 200Ω = " 100 200 R-SERIES . ."  Ω" CR
."   470Ω + 330Ω = " 470 330 R-SERIES . ."  Ω" CR
CR

."   Three in series: R1 + R2 + R3:" CR
."   100Ω + 200Ω + 300Ω = " 100 200 + 300 + . ."  Ω" CR
CR

\ ═══════════════════════════════════════
\ ENERGY CONVERSIONS
\ ═══════════════════════════════════════

: KWH-TO-BTU  ( kwh -- btu )  3412 * ;
: HP-TO-WATTS ( hp -- watts )  746 * ;

."  ENERGY CONVERSIONS" CR
DIVIDER

."   Kilowatt-hours → BTU:" CR
1 DUP . ."  kWh = " KWH-TO-BTU . ."  BTU" CR
5 DUP . ."  kWh = " KWH-TO-BTU . ."  BTU" CR
10 DUP . ."  kWh = " KWH-TO-BTU . ."  BTU" CR
CR

."   Horsepower → Watts:" CR
1 DUP . ."  HP = " HP-TO-WATTS . ."  W" CR
5 DUP . ."  HP = " HP-TO-WATTS . ."  W" CR
150 DUP . ."  HP = " HP-TO-WATTS . ."  W" CR
CR

\ ═══════════════════════════════════════
\ SPEED CONVERSIONS
\ ═══════════════════════════════════════

: MPH-TO-KPH  ( mph -- kph )  161 * 100 / ;
: KNOTS-TO-MPH ( knots -- mph*10 )  1151 * 1000 / ;

."  SPEED CONVERSIONS" CR
DIVIDER

."   MPH → KPH:" CR
30 DUP . ."  mph = " MPH-TO-KPH . ."  kph" CR
60 DUP . ."  mph = " MPH-TO-KPH . ."  kph" CR
100 DUP . ."  mph = " MPH-TO-KPH . ."  kph" CR
CR

."   Knots → MPH (x10):" CR
10 DUP . ."  knots = " KNOTS-TO-MPH . ."  (x10 mph)" CR
100 DUP . ."  knots = " KNOTS-TO-MPH . ."  (x10 mph)" CR
CR

\ ═══════════════════════════════════════
\ PRACTICAL CALCULATIONS
\ ═══════════════════════════════════════

."  PRACTICAL CALCULATIONS" CR
DIVIDER

."   Monthly electricity cost:" CR
."   Usage: 900 kWh at $0.12/kWh" CR
."   Cost: $" 900 12 * 100 / . CR
CR

."   Fuel economy:" CR
."   350 miles on 14 gallons:" CR
."   MPG = " 350 14 / . CR
CR

."   Wire gauge load (simplified):" CR
."   14 AWG max: 15A at 120V = " 15 120 * . ."  watts" CR
."   12 AWG max: 20A at 120V = " 20 120 * . ."  watts" CR
."   10 AWG max: 30A at 240V = " 30 240 * . ."  watts" CR
CR

HEADER
."  Engineering Unit Converter Complete" CR
HEADER
