REM ═══════════════════════════════════════════════════════
REM   PERSONAL FINANCE CALCULATOR
REM   A practical financial planning tool
REM   Computes compound interest, loan payments,
REM   investment growth, and savings projections
REM ═══════════════════════════════════════════════════════

PRINT "╔═══════════════════════════════════════════════════╗"
PRINT "║       PERSONAL FINANCE CALCULATOR v1.0            ║"
PRINT "╚═══════════════════════════════════════════════════╝"
PRINT ""

REM ─── SECTION 1: COMPOUND INTEREST CALCULATOR ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 1: COMPOUND INTEREST ON SAVINGS"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET principal = 10000
LET annual_rate = 0.055
LET years = 10
LET compounds_per_year = 12

PRINT "  Initial Deposit:     $"; principal
PRINT "  Annual Rate:          "; annual_rate * 100; "%"
PRINT "  Compounding:          Monthly"
PRINT "  Investment Period:    "; years; " years"
PRINT ""

REM Calculate compound interest: A = P(1 + r/n)^(nt)
LET rate_per_period = annual_rate / compounds_per_year
LET total_periods = compounds_per_year * years

DIM balances(10)

PRINT "  Year    Balance         Interest Earned"
PRINT "  ────    ───────         ───────────────"

FOR yr = 1 TO years
    LET periods = compounds_per_year * yr
    LET balance = principal * (1 + rate_per_period) ^ periods
    LET interest_earned = balance - principal
    LET balances(yr) = INT(balance)
    PRINT "   "; yr; "     $"; INT(balance * 100) / 100; "       $"; INT(interest_earned * 100) / 100
NEXT yr

LET final_balance = principal * (1 + rate_per_period) ^ total_periods
LET total_interest = final_balance - principal
PRINT ""
PRINT "  ► Final Balance:     $"; INT(final_balance * 100) / 100
PRINT "  ► Total Interest:    $"; INT(total_interest * 100) / 100
PRINT "  ► Return on Investment: "; INT(total_interest / principal * 10000) / 100; "%"
PRINT ""

REM ─── SECTION 2: LOAN PAYMENT CALCULATOR ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 2: LOAN PAYMENT CALCULATOR"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET loan_amount = 250000
LET loan_rate = 0.065
LET loan_years = 30

PRINT "  Loan Amount:         $"; loan_amount
PRINT "  Annual Rate:          "; loan_rate * 100; "%"
PRINT "  Loan Term:            "; loan_years; " years"
PRINT ""

REM Monthly payment formula: M = P[r(1+r)^n] / [(1+r)^n - 1]
LET monthly_rate = loan_rate / 12
LET num_payments = loan_years * 12
LET rate_factor = (1 + monthly_rate) ^ num_payments
LET monthly_payment = loan_amount * (monthly_rate * rate_factor) / (rate_factor - 1)

PRINT "  ► Monthly Payment:   $"; INT(monthly_payment * 100) / 100
LET total_paid = monthly_payment * num_payments
LET total_loan_interest = total_paid - loan_amount
PRINT "  ► Total Paid:        $"; INT(total_paid * 100) / 100
PRINT "  ► Total Interest:    $"; INT(total_loan_interest * 100) / 100
PRINT "  ► Interest Ratio:     "; INT(total_loan_interest / loan_amount * 10000) / 100; "%"
PRINT ""

REM Amortization schedule (first 5 years, annually)
PRINT "  AMORTIZATION SUMMARY (Annual)"
PRINT "  Year   Principal Paid   Interest Paid   Balance"
PRINT "  ────   ──────────────   ─────────────   ───────"

LET remaining = loan_amount
FOR yr = 1 TO 5
    LET year_principal = 0
    LET year_interest = 0
    FOR mo = 1 TO 12
        LET interest_portion = remaining * monthly_rate
        LET principal_portion = monthly_payment - interest_portion
        LET year_interest = year_interest + interest_portion
        LET year_principal = year_principal + principal_portion
        LET remaining = remaining - principal_portion
    NEXT mo
    PRINT "   "; yr; "    $"; INT(year_principal); "         $"; INT(year_interest); "       $"; INT(remaining)
NEXT yr

PRINT ""

REM ─── SECTION 3: INVESTMENT COMPARISON ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 3: INVESTMENT GROWTH COMPARISON"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET invest_amount = 500
PRINT "  Monthly Investment: $"; invest_amount
PRINT "  Comparing 3 scenarios over 20 years:"
PRINT ""

REM Scenario 1: Conservative (3%)
LET r1 = 0.03 / 12
LET n = 240
LET fv1 = invest_amount * ((1 + r1) ^ n - 1) / r1
PRINT "  Conservative (3%):  $"; INT(fv1)

REM Scenario 2: Moderate (7%)
LET r2 = 0.07 / 12
LET fv2 = invest_amount * ((1 + r2) ^ n - 1) / r2
PRINT "  Moderate (7%):      $"; INT(fv2)

REM Scenario 3: Aggressive (10%)
LET r3 = 0.10 / 12
LET fv3 = invest_amount * ((1 + r3) ^ n - 1) / r3
PRINT "  Aggressive (10%):   $"; INT(fv3)

LET total_invested = invest_amount * n
PRINT ""
PRINT "  Total Contributed:  $"; INT(total_invested)
PRINT ""

REM Bar chart comparison
PRINT "  GROWTH COMPARISON CHART"
PRINT "  ──────────────────────────────────────────"
LET max_val = fv3
LET bar_width = 40

LET bar_len = INT(fv1 / max_val * bar_width)
PRINT "  3%  │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; INT(fv1)

LET bar_len = INT(fv2 / max_val * bar_width)
PRINT "  7%  │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; INT(fv2)

LET bar_len = INT(fv3 / max_val * bar_width)
PRINT "  10% │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; INT(fv3)

PRINT "  ──────────────────────────────────────────"
PRINT ""

REM ─── SECTION 4: SAVINGS GOAL PLANNER ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 4: SAVINGS GOAL PLANNER"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET goal = 50000
LET current_savings = 5000
LET monthly_save = 750
LET save_rate = 0.04

PRINT "  Savings Goal:        $"; goal
PRINT "  Current Savings:     $"; current_savings
PRINT "  Monthly Contribution: $"; monthly_save
PRINT "  Annual Return:        "; save_rate * 100; "%"
PRINT ""

LET balance = current_savings
LET r = save_rate / 12
LET months_needed = 0

WHILE balance < goal AND months_needed < 600
    LET balance = balance * (1 + r) + monthly_save
    LET months_needed = months_needed + 1
WEND

LET years_needed = INT(months_needed / 12)
LET remaining_months = months_needed - (years_needed * 12)

PRINT "  ► Time to Goal:      "; years_needed; " years, "; remaining_months; " months"
PRINT "  ► Total Contributed:  $"; INT(current_savings + monthly_save * months_needed)
PRINT "  ► Interest Earned:    $"; INT(balance - current_savings - monthly_save * months_needed)
PRINT "  ► Final Balance:      $"; INT(balance)
PRINT ""

REM ─── SECTION 5: RETIREMENT PROJECTION ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 5: RETIREMENT PROJECTION"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET current_age = 30
LET retire_age = 65
LET current_401k = 25000
LET monthly_contrib = 800
LET employer_match = 0.50
LET match_limit = 0.06
LET salary = 75000
LET growth_rate = 0.07

PRINT "  Current Age:          "; current_age
PRINT "  Retirement Age:       "; retire_age
PRINT "  Current 401(k):      $"; current_401k
PRINT "  Monthly Contribution: $"; monthly_contrib
PRINT "  Employer Match:       "; employer_match * 100; "% up to "; match_limit * 100; "% of salary"
PRINT "  Expected Return:      "; growth_rate * 100; "%"
PRINT ""

LET monthly_match = salary * match_limit / 12 * employer_match
IF monthly_match > monthly_contrib * employer_match THEN
    LET monthly_match = monthly_contrib * employer_match
END IF
LET total_monthly = monthly_contrib + monthly_match

PRINT "  Employer Match/mo:   $"; INT(monthly_match)
PRINT "  Total Monthly:       $"; INT(total_monthly)
PRINT ""

LET retire_balance = current_401k
LET r = growth_rate / 12
LET retire_months = (retire_age - current_age) * 12

FOR mo = 1 TO retire_months
    LET retire_balance = retire_balance * (1 + r) + total_monthly
NEXT mo

PRINT "  ► Projected 401(k) at "; retire_age; ":  $"; INT(retire_balance)
LET annual_withdrawal = retire_balance * 0.04
PRINT "  ► Safe Annual Withdrawal (4%):  $"; INT(annual_withdrawal)
PRINT "  ► Monthly Income in Retirement: $"; INT(annual_withdrawal / 12)
PRINT ""

REM ─── SUMMARY ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  FINANCIAL PLANNING SUMMARY"
PRINT "═══════════════════════════════════════════════════"
PRINT ""
PRINT "  ✓ Savings with compound interest grow faster"
PRINT "    than you might expect - start early!"
PRINT "  ✓ A 30-year mortgage nearly doubles the cost"
PRINT "    of a home through interest payments"
PRINT "  ✓ The difference between 3% and 10% returns"
PRINT "    over 20 years is dramatic"
PRINT "  ✓ Employer 401(k) matching is free money -"
PRINT "    always contribute enough to get the full match"
PRINT ""
PRINT "═══════════════════════════════════════════════════"
PRINT "  Finance Calculator Complete"
PRINT "═══════════════════════════════════════════════════"
END
