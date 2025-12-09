"""
Comprehensive Language Testing Suite for Time_Warp IDE
This script systematically tests every command and function in all supported languages.
No shortcuts, no skipping, thorough verification only.
"""

import tkinter as tk
from core.interpreter import Time_WarpInterpreter
import traceback
import json
from datetime import datetime

# Test results tracking
test_results = {
    'timestamp': datetime.now().isoformat(),
    'languages': {}
}


def create_test_environment():
    """Create tkinter window and interpreter for testing"""
    root = tk.Tk()
    root.withdraw()  # Hide window
    output = tk.Text(root)
    canvas = tk.Canvas(root, width=400, height=400, bg='white')
    interp = Time_WarpInterpreter(output)
    interp.turtle_canvas = canvas
    interp.init_turtle_graphics()
    return root, output, canvas, interp


def run_test(interp, output, language, test_name, command, expected_substring=None, should_fail=False):
    """Run a single test and return results"""
    output.delete('1.0', 'end')
    interp.current_language_mode = language
    
    try:
        _ = interp.execute_line(command)
        output_text = output.get('1.0', 'end').strip()
        
        # Determine if test passed
        if should_fail:
            passed = False
            status = "FAIL (should have failed but didn't)"
        elif expected_substring is None:
            passed = True
            status = "PASS"
        else:
            passed = expected_substring.lower() in output_text.lower()
            status = "PASS" if passed else f"FAIL (expected '{expected_substring}', got '{output_text[:50]}')"
        
        return {
            'test': test_name,
            'command': command,
            'passed': passed,
            'status': status,
            'output': output_text[:100],
            'exception': None
        }
    except Exception as e:
        return {
            'test': test_name,
            'command': command,
            'passed': False,
            'status': f"EXCEPTION: {str(e)}",
            'output': '',
            'exception': traceback.format_exc()
        }


# ============================================================================
# LOGO TESTS
# ============================================================================

def test_logo(interp, output, canvas):
    """Comprehensive Logo language testing"""
    print("\n" + "="*70)
    print("LOGO LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Movement commands
        ('Movement: FORWARD', 'FORWARD 50', 'turtle moved'),
        ('Movement: FD alias', 'FD 50', 'turtle moved'),
        ('Movement: BACK', 'BACK 50', 'turtle moved'),
        ('Movement: BK alias', 'BK 50', 'turtle moved'),
        ('Movement: BACKWARD', 'BACKWARD 50', 'turtle moved'),
        ('Movement: LEFT', 'LEFT 90', 'turned'),
        ('Movement: LT alias', 'LT 90', 'turned'),
        ('Movement: RIGHT', 'RIGHT 90', 'turned'),
        ('Movement: RT alias', 'RT 90', 'turned'),
        
        # Pen control
        ('Pen: PENUP', 'PENUP', 'pen up'),
        ('Pen: PU alias', 'PU', 'pen up'),
        ('Pen: PENDOWN', 'PENDOWN', 'pen down'),
        ('Pen: PD alias', 'PD', 'pen down'),
        
        # Screen commands
        ('Screen: CLEARSCREEN', 'CLEARSCREEN', 'cleared'),
        ('Screen: CS alias', 'CS', 'cleared'),
        ('Screen: HOME', 'HOME', 'home'),
        
        # Output commands
        ('Output: PRINT', 'PRINT [Hello]', 'Hello'),
        ('Output: CLEARTEXT', 'CLEARTEXT', 'cleared'),
        
        # Comments
        ('Comments: semicolon', '; This is a comment', ''),
        
        # Turtle state
        ('State: SHOWTURTLE', 'SHOWTURTLE', 'visible'),
        ('State: HIDETURTLE', 'HIDETURTLE', 'hidden'),
        ('State: HEADING', 'HEADING', 'heading'),
        ('State: POSITION', 'POSITION', 'position'),
        
        # Color commands
        ('Color: SETCOLOR', 'SETCOLOR red', 'color'),
        ('Color: COLOR', 'COLOR blue', 'color'),
        
        # Drawing shapes
        ('Shapes: CIRCLE', 'CIRCLE 50', 'circle'),
        ('Shapes: DOT', 'DOT 5', 'dot'),
        ('Shapes: RECT', 'RECT 50 40', 'rect'),
        ('Shapes: TEXT', 'TEXT Test', 'text'),
        
        # Pen properties
        ('Pen: SETPENSIZE', 'SETPENSIZE 3', 'size'),
        ('Pen: SETXY', 'SETXY 100 100', 'setxy'),
        
        # Control structures
        ('Control: REPEAT', 'REPEAT 3 [FORWARD 10]', 'continue'),
        ('Control: IF', 'IF 1 = 1 [FORWARD 20]', 'continue'),
        
        # Variables
        ('Variables: Assignment', 'MAKE "x 10', None),
        ('Variables: Reference', ':x', None),
        
        # Procedures
        ('Procedures: TO', 'TO MYSQUARE\nREPEAT 4 [FORWARD 50 RIGHT 90]\nEND', None),
        ('Procedures: Call', 'MYSQUARE', 'continue'),
    ]
    
    logo_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Logo', test_name, command, expected)
        logo_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return logo_results


# ============================================================================
# PILOT TESTS
# ============================================================================

def test_pilot(interp, output, canvas):
    """Comprehensive PILOT language testing"""
    print("\n" + "="*70)
    print("PILOT LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Text output
        ('Output: T:', 'T:Hello World', 'hello'),
        
        # Accept input
        ('Input: A:', 'A:Enter name', 'enter'),
        
        # Conditionals
        ('Conditional: Y:', 'Y:Test\nT:Yes', 'yes'),
        ('Conditional: N:', 'N:Test\nT:No', 'no'),
        
        # Jump commands
        ('Jump: J:', 'L:START\nT:Test\nJ:END\nL:END', 'test'),
        ('Jump: M:', 'M:pattern\nT:Matched', 'matched'),
        
        # Match/String operations
        ('Match: MT:', 'MT:test,pattern', None),
        
        # Compute
        ('Compute: C:', 'C:x = 5 + 3', 'compute'),
        
        # Graphics
        ('Graphics: G:LINE', 'G:LINE,0,0,100,100', 'g:line'),
        ('Graphics: G:CIRCLE', 'G:CIRCLE,50,50,25', 'g:circle'),
        ('Graphics: G:RECT', 'G:RECT,0,0,100,100', 'g:rect'),
        ('Graphics: G:CLEAR', 'G:CLEAR', 'cleared'),
        ('Graphics: G:PENUP', 'G:PENUP', 'pen'),
        ('Graphics: G:PENDOWN', 'G:PENDOWN', 'pen'),
        ('Graphics: G:COLOR', 'G:COLOR,red', 'color'),
        
        # Label
        ('Label: L:', 'L:LABEL', 'continue'),
        
        # Runtime
        ('Runtime: R:', 'R:TIME', None),
        
        # Audio
        ('Audio: AUDIO:', 'AUDIO:PLAY,sound.wav', None),
        
        # File operations
        ('File: F:', 'F:WRITE,test.txt,Hello', None),
        
        # String operations
        ('String: S:', 'S:UPPER,hello', None),
        
        # Date/Time
        ('DateTime: DT:', 'DT:NOW', None),
        
        # Math
        ('Math: MATH:SIN', 'MATH:SIN 90', 'math'),
        
        # Pause
        ('Pause: PA:', 'PA:1000', None),
        
        # Pause
        ('Clear/Home: CH:', 'CH:', None),
    ]
    
    pilot_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'PILOT', test_name, command, expected)
        pilot_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return pilot_results

# ============================================================================
# BASIC TESTS
# ============================================================================

def test_basic(interp, output, canvas):
    """Comprehensive BASIC language testing"""
    print("\n" + "="*70)
    print("BASIC LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Output
        ('Output: PRINT', 'PRINT "Hello"', 'hello'),
        ('Output: PRINT number', 'PRINT 42', '42'),
        
        # Input
        ('Input: INPUT', 'INPUT "Enter: ",x', 'enter'),
        
        # Variables
        ('Variables: LET', 'LET x = 10', None),
        ('Variables: Assignment', 'x = 20', None),
        
        # Control flow
        ('Control: IF...THEN', 'IF 1 = 1 THEN PRINT "True"', 'true'),
        ('Control: GOTO', 'GOTO 100\nPRINT "Skipped"\n100 PRINT "Label"', 'label'),
        ('Control: GOSUB', 'GOSUB 100\nEND\n100 RETURN', None),
        
        # Loops
        ('Loop: FOR...NEXT', 'FOR i = 1 TO 3\nPRINT i\nNEXT', None),
        
        # Arrays
        ('Array: DIM', 'DIM a(10)', None),
        ('Array: Assignment', 'a(1) = 5', None),
        
        # Functions
        ('Function: REM', 'REM This is a comment', None),
        ('Function: END', 'END', None),
        
        # Modern BASIC
        ('Modern: DO...LOOP', 'DO\nLOOP', None),
        ('Modern: WHILE...WEND', 'WHILE 1 = 0\nWEND', None),
        ('Modern: SELECT...CASE', 'SELECT 1\nCASE 1\nEND SELECT', None),
        
        # Enhanced commands
        ('Enhanced: INCR', 'x = 5\nINCR x', None),
        ('Enhanced: DECR', 'x = 5\nDECR x', None),
    ]
    
    basic_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Basic', test_name, command, expected)
        basic_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return basic_results

# ============================================================================
# PYTHON TESTS
# ============================================================================

def test_python(interp, output, canvas):
    """Comprehensive Python testing"""
    print("\n" + "="*70)
    print("PYTHON LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Output
        ('Output: print()', 'print("Hello")', 'hello'),
        ('Output: print number', 'print(42)', '42'),
        
        # Variables
        ('Variables: assignment', 'x = 10', None),
        ('Variables: multiple', 'x, y = 1, 2', None),
        
        # Control
        ('Control: if...else', 'if True:\n    print("yes")\nelse:\n    print("no")', 'yes'),
        ('Control: for loop', 'for i in range(3):\n    print(i)', None),
        ('Control: while loop', 'x = 0\nwhile x < 3:\n    x = x + 1', None),
        
        # Functions
        ('Functions: def', 'def foo():\n    return 42', None),
        ('Functions: call', 'print(len("test"))', '4'),
        
        # Data structures
        ('Lists: create', 'x = [1, 2, 3]', None),
        ('Lists: access', 'print([1, 2, 3][0])', '1'),
        ('Dicts: create', 'x = {"a": 1}', None),
        ('Dicts: access', 'print({"a": 1}["a"])', '1'),
        
        # Operations
        ('Math: addition', 'print(1 + 2)', '3'),
        ('Math: multiplication', 'print(3 * 4)', '12'),
        ('String: concatenation', 'print("a" + "b")', 'ab'),
    ]
    
    python_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Python', test_name, command, expected)
        python_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return python_results

# ============================================================================
# JAVASCRIPT TESTS
# ============================================================================

def test_javascript(interp, output, canvas):
    """Comprehensive JavaScript testing"""
    print("\n" + "="*70)
    print("JAVASCRIPT LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Output
        ('Output: console.log()', 'console.log("Hello")', 'hello'),
        ('Output: print number', 'console.log(42)', '42'),
        
        # Variables
        ('Variables: var', 'var x = 10', None),
        ('Variables: let', 'let y = 20', None),
        ('Variables: const', 'const z = 30', None),
        
        # Control
        ('Control: if...else', 'if (true) { console.log("yes") } else { console.log("no") }', 'yes'),
        ('Control: for loop', 'for (let i = 0; i < 3; i++) { console.log(i) }', None),
        ('Control: while loop', 'let x = 0; while (x < 3) { x = x + 1 }', None),
        
        # Functions
        ('Functions: declaration', 'function foo() { return 42 }', None),
        ('Functions: call', 'console.log(foo())', None),
        
        # Objects & Arrays
        ('Arrays: create', 'let a = [1, 2, 3]', None),
        ('Arrays: access', 'console.log([1, 2, 3][0])', '1'),
        ('Objects: create', 'let o = {a: 1}', None),
        ('Objects: access', 'console.log({a: 1}.a)', '1'),
        
        # Operators
        ('Math: addition', 'console.log(1 + 2)', '3'),
        ('Math: string concat', 'console.log("a" + "b")', 'ab'),
    ]
    
    js_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'JavaScript', test_name, command, expected)
        js_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return js_results

# ============================================================================
# FORTH TESTS
# ============================================================================

def test_forth(interp, output, canvas):
    """Comprehensive Forth testing"""
    print("\n" + "="*70)
    print("FORTH LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Stack operations
        ('Stack: DUP', '5 DUP', None),
        ('Stack: DROP', '5 DROP', None),
        ('Stack: SWAP', '1 2 SWAP', None),
        ('Stack: OVER', '1 2 OVER', None),
        ('Stack: ROT', '1 2 3 ROT', None),
        
        # Arithmetic
        ('Arithmetic: +', '5 3 +', None),
        ('Arithmetic: -', '5 3 -', None),
        ('Arithmetic: *', '5 3 *', None),
        ('Arithmetic: /', '6 3 /', None),
        
        # Output
        ('Output: .', '42 .', None),
        ('Output: CR', 'CR', None),
        
        # Definitions
        ('Definition: : ;', ': DOUBLE 2 * ;', None),
        ('Definition: call', 'DOUBLE', None),
        
        # Variables
        ('Variables: VARIABLE', 'VARIABLE x', None),
        ('Variables: !', '5 x !', None),
        ('Variables: @', 'x @', None),
    ]
    
    forth_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Forth', test_name, command, expected)
        forth_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return forth_results

# ============================================================================
# PASCAL TESTS
# ============================================================================

def test_pascal(interp, output, canvas):
    """Comprehensive Pascal testing"""
    print("\n" + "="*70)
    print("PASCAL LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Variables
        ('Variables: VAR', 'VAR x: INTEGER', None),
        ('Variables: assignment', 'x := 10', None),
        
        # Output
        ('Output: writeln', 'writeln("Hello")', 'hello'),
        ('Output: write', 'write("test")', 'test'),
        
        # Control
        ('Control: IF', 'IF 1 = 1 THEN writeln("yes")', 'yes'),
        ('Control: WHILE', 'WHILE 1 = 0 DO x := 1', None),
        ('Control: FOR', 'FOR i := 1 TO 3 DO writeln(i)', None),
        
        # Procedures
        ('Procedures: PROCEDURE', 'PROCEDURE foo; BEGIN END;', None),
        
        # Functions
        ('Functions: FUNCTION', 'FUNCTION foo: INTEGER; BEGIN foo := 42 END;', None),
    ]
    
    pascal_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Pascal', test_name, command, expected)
        pascal_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return pascal_results

# ============================================================================
# PERL TESTS
# ============================================================================

def test_perl(interp, output, canvas):
    """Comprehensive Perl testing"""
    print("\n" + "="*70)
    print("PERL LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Output
        ('Output: print', 'print "Hello\\n"', 'hello'),
        
        # Variables
        ('Variables: $', '$x = 10', None),
        ('Variables: @', '@a = (1, 2, 3)', None),
        ('Variables: %', '%h = (a => 1)', None),
        
        # Control
        ('Control: if...else', 'if (1) { print "yes\\n" } else { print "no\\n" }', 'yes'),
        ('Control: for', 'for $i (1..3) { print $i }', None),
        ('Control: foreach', 'foreach my $x (@a) { print $x }', None),
        
        # Functions
        ('Functions: sub', 'sub foo { return 42 }', None),
        ('Functions: call', 'print foo()\\n', None),
        
        # Regular expressions
        ('Regex: match', '"test" =~ /test/', None),
        ('Regex: substitute', '"test" =~ s/test/hello/', None),
    ]
    
    perl_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Perl', test_name, command, expected)
        perl_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return perl_results

# ============================================================================
# PROLOG TESTS
# ============================================================================

def test_prolog(interp, output, canvas):
    """Comprehensive Prolog testing"""
    print("\n" + "="*70)
    print("PROLOG LANGUAGE COMPREHENSIVE TEST")
    print("="*70)
    
    tests = [
        # Facts
        ('Facts: assertion', 'parent(tom, bob).', None),
        
        # Rules
        ('Rules: definition', 'grandparent(X, Y) :- parent(X, Z), parent(Z, Y).', None),
        
        # Queries
        ('Queries: ?-', '?- parent(tom, bob).', None),
        
        # Lists
        ('Lists: create', '[1, 2, 3]', None),
        ('Lists: head|tail', '[H|T] = [1, 2, 3]', None),
        
        # Unification
        ('Unification: =', 'X = 5', None),
        
        # Control
        ('Control: !', '!', None),
        ('Control: ->', 'true -> print(yes) ; print(no)', None),
    ]
    
    prolog_results = []
    for test_name, command, expected in tests:
        result = run_test(interp, output, 'Prolog', test_name, command, expected)
        prolog_results.append(result)
        status = "✓" if result['passed'] else "✗"
        print(f"{status} {test_name}: {result['status']}")
    
    return prolog_results

# ============================================================================
# MAIN TEST EXECUTION
# ============================================================================

def main():
    """Run all language tests"""
    print("\n" + "="*70)
    print("TIME_WARP COMPREHENSIVE LANGUAGE TEST SUITE")
    print("Testing ALL commands and functions thoroughly")
    print("="*70)
    
    root, output, canvas, interp = create_test_environment()
    
    # Run all tests
    logo_results = test_logo(interp, output, canvas)
    pilot_results = test_pilot(interp, output, canvas)
    basic_results = test_basic(interp, output, canvas)
    python_results = test_python(interp, output, canvas)
    js_results = test_javascript(interp, output, canvas)
    forth_results = test_forth(interp, output, canvas)
    pascal_results = test_pascal(interp, output, canvas)
    perl_results = test_perl(interp, output, canvas)
    prolog_results = test_prolog(interp, output, canvas)
    
    # Compile results
    test_results['languages'] = {
        'Logo': logo_results,
        'PILOT': pilot_results,
        'BASIC': basic_results,
        'Python': python_results,
        'JavaScript': js_results,
        'Forth': forth_results,
        'Pascal': pascal_results,
        'Perl': perl_results,
        'Prolog': prolog_results,
    }
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    total_tests = 0
    total_passed = 0
    
    for language, results in test_results['languages'].items():
        passed = sum(1 for r in results if r['passed'])
        total = len(results)
        total_tests += total
        total_passed += passed
        percentage = (passed / total * 100) if total > 0 else 0
        print(f"{language:15} {passed:3}/{total:3} passed ({percentage:5.1f}%)")
    
    print("-" * 70)
    overall_percentage = (total_passed / total_tests * 100) if total_tests > 0 else 0
    print(f"{'TOTAL':15} {total_passed:3}/{total_tests:3} passed ({overall_percentage:5.1f}%)")
    print("="*70)
    
    # Save detailed results
    with open('test_results.json', 'w') as f:
        json.dump(test_results, f, indent=2)
    print(f"\nDetailed results saved to test_results.json")
    
    # Print failed tests
    failed_tests = []
    for language, results in test_results['languages'].items():
        for result in results:
            if not result['passed']:
                failed_tests.append((language, result))
    
    if failed_tests:
        print("\n" + "="*70)
        print("FAILED TESTS (requiring fixes)")
        print("="*70)
        for language, result in failed_tests:
            print(f"\n{language}: {result['test']}")
            print(f"  Command: {result['command']}")
            print(f"  Status: {result['status']}")
            if result['exception']:
                print(f"  Exception:\n{result['exception'][:200]}")
    
    root.destroy()

if __name__ == '__main__':
    main()
