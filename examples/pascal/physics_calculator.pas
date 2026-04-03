PROGRAM PhysicsCalculator;

{ ═══════════════════════════════════════════════════ }
{ PHYSICS FORMULA CALCULATOR                         }
{ Projectile motion, waves, energy, and orbital      }
{ mechanics calculations with tabular output         }
{ ═══════════════════════════════════════════════════ }

CONST G = 9.81;
CONST PI = 3.14159265;
CONST C = 299792458;
CONST PLANCK = 6.626e-34;
CONST BOLTZMANN = 1.381e-23;

VAR I : INTEGER;
VAR ANGLE_RAD : REAL;
VAR RANGE : REAL;
VAR MAX_HEIGHT : REAL;
VAR FLIGHT_TIME : REAL;
VAR V0 : REAL;

WRITELN('════════════════════════════════════════════════════════════');
WRITELN('              PHYSICS FORMULA CALCULATOR v1.0');
WRITELN('════════════════════════════════════════════════════════════');
WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 1: PROJECTILE MOTION           }
{ ═══════════════════════════════════════ }

V0 := 50;

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  PROJECTILE MOTION (Launch velocity = ', V0, ' m/s)');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Angle   Range(m)    Max Height(m)   Flight Time(s)');
WRITELN('  ─────   ────────    ─────────────   ──────────────');

FOR I := 10 TO 90 DO WRITELN('  ', I, '       ', ROUND(V0 * V0 * SIN(2 * I * PI / 180) / G), '          ', ROUND(V0 * V0 * SIN(I * PI / 180) * SIN(I * PI / 180) / (2 * G)), '             ', ROUND(2 * V0 * SIN(I * PI / 180) / G * 10) / 10);

WRITELN('');
WRITELN('  Optimal launch angle: 45 degrees');
WRITELN('  Maximum range at 45: ', ROUND(V0 * V0 / G), ' meters');
WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 2: FREE FALL                   }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  FREE FALL TABLE (no air resistance)');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Time(s)   Velocity(m/s)   Distance(m)');
WRITELN('  ───────   ─────────────   ───────────');

FOR I := 1 TO 10 DO WRITELN('  ', I, '         ', ROUND(G * I), '              ', ROUND(0.5 * G * I * I));

WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 3: WAVE PROPERTIES             }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  ELECTROMAGNETIC SPECTRUM');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');

VAR WAVELENGTH : REAL;
VAR FREQUENCY : REAL;
VAR ENERGY : REAL;

WRITELN('  Radio Waves:');
WAVELENGTH := 1.0;
FREQUENCY := C / WAVELENGTH;
WRITELN('    Wavelength: ', WAVELENGTH, ' m  Frequency: ', FREQUENCY, ' Hz');

WRITELN('  Microwaves:');
WAVELENGTH := 0.01;
FREQUENCY := C / WAVELENGTH;
WRITELN('    Wavelength: ', WAVELENGTH, ' m  Frequency: ', FREQUENCY, ' Hz');

WRITELN('  Infrared:');
WAVELENGTH := 0.001;
FREQUENCY := C / WAVELENGTH;
WRITELN('    Wavelength: ', WAVELENGTH, ' m  Frequency: ', FREQUENCY, ' Hz');

WRITELN('  Visible Light (green):');
WAVELENGTH := 5.5e-7;
FREQUENCY := C / WAVELENGTH;
WRITELN('    Wavelength: ', WAVELENGTH, ' m  Frequency: ', FREQUENCY, ' Hz');

WRITELN('  Ultraviolet:');
WAVELENGTH := 1.0e-8;
FREQUENCY := C / WAVELENGTH;
WRITELN('    Wavelength: ', WAVELENGTH, ' m  Frequency: ', FREQUENCY, ' Hz');

WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 4: KINETIC ENERGY TABLE        }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  KINETIC ENERGY (mass = 1 kg)');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Speed(m/s)   KE(J)     Momentum(kg m/s)');
WRITELN('  ──────────   ─────     ────────────────');

FOR I := 1 TO 20 DO WRITELN('  ', I * 5, '          ', ROUND(0.5 * I * 5 * I * 5), '        ', I * 5);

WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 5: PENDULUM PERIODS            }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  SIMPLE PENDULUM PERIODS');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Length(m)   Period(s)   Frequency(Hz)');
WRITELN('  ─────────   ─────────   ─────────────');

FOR I := 1 TO 10 DO WRITELN('  ', I * 0.25, '        ', ROUND(2 * PI * SQRT(I * 0.25 / G) * 1000) / 1000, '       ', ROUND(1 / (2 * PI * SQRT(I * 0.25 / G)) * 1000) / 1000);

WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 6: ORBITAL VELOCITY            }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  ORBITAL MECHANICS');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');

VAR EARTH_RADIUS : REAL;
VAR EARTH_MASS : REAL;
VAR GRAV_CONST : REAL;
VAR ORBIT_V : REAL;
VAR ORBIT_PERIOD : REAL;

EARTH_RADIUS := 6371000;
GRAV_CONST := 6.674e-11;
EARTH_MASS := 5.972e24;

WRITELN('  Earth Radius: 6371 km');
WRITELN('  Earth Mass: 5.972 x 10^24 kg');
WRITELN('');
WRITELN('  Altitude(km)   Orbital Velocity(m/s)   Period(min)');
WRITELN('  ────────────   ─────────────────────   ───────────');

FOR I := 1 TO 10 DO WRITELN('  ', I * 200, '            ', ROUND(SQRT(GRAV_CONST * EARTH_MASS / (EARTH_RADIUS + I * 200000))), '                   ', ROUND(2 * PI * (EARTH_RADIUS + I * 200000) / SQRT(GRAV_CONST * EARTH_MASS / (EARTH_RADIUS + I * 200000)) / 60));

WRITELN('');

{ ═══════════════════════════════════════ }
{ SECTION 7: TRIGONOMETRIC TABLE         }
{ ═══════════════════════════════════════ }

WRITELN('────────────────────────────────────────────────────────────');
WRITELN('  TRIGONOMETRIC FUNCTION TABLE');
WRITELN('────────────────────────────────────────────────────────────');
WRITELN('');
WRITELN('  Angle   SIN        COS        TAN');
WRITELN('  ─────   ────       ────       ────');

FOR I := 0 TO 12 DO WRITELN('  ', I * 15, '     ', ROUND(SIN(I * 15 * PI / 180) * 10000) / 10000, '    ', ROUND(COS(I * 15 * PI / 180) * 10000) / 10000, '    ', ROUND(TAN(I * 15 * PI / 180) * 10000) / 10000);

WRITELN('');
WRITELN('════════════════════════════════════════════════════════════');
WRITELN('  Physics Calculator Complete');
WRITELN('  Constants: g=9.81 m/s^2  c=299792458 m/s  pi=3.14159');
WRITELN('════════════════════════════════════════════════════════════');

END.
