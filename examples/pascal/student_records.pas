program PascalDemo;
{ Pascal Structured Programming Demo }
{ Demonstrates procedures, functions, and control structures }

uses crt;

type
    TStudent = record
        name: string[50];
        age: integer;
        grade: char;
    end;

var
    students: array[1..4] of TStudent;
    i, total_age: integer;
    avg_age: real;

procedure InitializeStudents;
begin
    students[1].name := 'Alice';
    students[1].age := 20;
    students[1].grade := 'A';

    students[2].name := 'Bob';
    students[2].age := 19;
    students[2].grade := 'B';

    students[3].name := 'Charlie';
    students[3].age := 21;
    students[3].grade := 'A';

    students[4].name := 'Diana';
    students[4].age := 20;
    students[4].grade := 'C';
end;

function CalculateAverageAge: real;
var
    i, sum: integer;
begin
    sum := 0;
    for i := 1 to 4 do
        sum := sum + students[i].age;
    CalculateAverageAge := sum / 4.0;
end;

procedure DisplayStudents;
var
    i: integer;
begin
    writeln('Student Records:');
    writeln('================');
    for i := 1 to 4 do
    begin
        writeln(i, '. ', students[i].name,
                ' (Age: ', students[i].age,
                ', Grade: ', students[i].grade, ')');
    end;
    writeln;
end;

procedure DisplayGradeDistribution;
var
    grade_a, grade_b, grade_c: integer;
    i: integer;
begin
    grade_a := 0;
    grade_b := 0;
    grade_c := 0;

    for i := 1 to 4 do
    begin
        case students[i].grade of
            'A': grade_a := grade_a + 1;
            'B': grade_b := grade_b + 1;
            'C': grade_c := grade_c + 1;
        end;
    end;

    writeln('Grade Distribution:');
    writeln('A: ', grade_a, ' students');
    writeln('B: ', grade_b, ' students');
    writeln('C: ', grade_c, ' students');
    writeln;
end;

begin
    clrscr;
    writeln('Pascal Structured Programming Demo');
    writeln('===================================');
    writeln;

    InitializeStudents;
    DisplayStudents;

    avg_age := CalculateAverageAge;
    writeln('Average age: ', avg_age:4:1, ' years');
    writeln;

    DisplayGradeDistribution;

    writeln('Demo complete! Press any key to exit.');
    readkey;
end.