REM ═══════════════════════════════════════════════════════
REM   SALES ANALYTICS DASHBOARD
REM   A business reporting tool that analyzes quarterly
REM   sales data across multiple product lines,
REM   generates charts, rankings, and trend analysis
REM ═══════════════════════════════════════════════════════

PRINT "╔═══════════════════════════════════════════════════╗"
PRINT "║       SALES ANALYTICS DASHBOARD v1.0              ║"
PRINT "║       Fiscal Year 2025 Report                     ║"
PRINT "╚═══════════════════════════════════════════════════╝"
PRINT ""

REM ─── LOAD SALES DATA ───
REM Product lines: Electronics, Software, Services, Hardware, Support
REM Quarters: Q1, Q2, Q3, Q4

DIM electronics(4)
DIM software(4)
DIM services(4)
DIM hardware(4)
DIM support(4)

REM Electronics quarterly sales (in thousands)
LET electronics(1) = 145
LET electronics(2) = 162
LET electronics(3) = 178
LET electronics(4) = 210

REM Software quarterly sales
LET software(1) = 230
LET software(2) = 255
LET software(3) = 280
LET software(4) = 310

REM Services quarterly sales
LET services(1) = 95
LET services(2) = 110
LET services(3) = 125
LET services(4) = 140

REM Hardware quarterly sales
LET hardware(1) = 180
LET hardware(2) = 168
LET hardware(3) = 155
LET hardware(4) = 172

REM Support quarterly sales
LET support(1) = 65
LET support(2) = 72
LET support(3) = 78
LET support(4) = 85

REM ─── SECTION 1: QUARTERLY BREAKDOWN ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 1: QUARTERLY SALES BREAKDOWN ($K)"
PRINT "═══════════════════════════════════════════════════"
PRINT ""
PRINT "  Product        Q1     Q2     Q3     Q4    Total"
PRINT "  ───────────  ─────  ─────  ─────  ─────  ──────"

LET e_total = SUM(electronics)
PRINT "  Electronics   "; electronics(1); "   "; electronics(2); "   "; electronics(3); "   "; electronics(4); "    "; e_total

LET s_total = SUM(software)
PRINT "  Software      "; software(1); "   "; software(2); "   "; software(3); "   "; software(4); "   "; s_total

LET sv_total = SUM(services)
PRINT "  Services       "; services(1); "   "; services(2); "   "; services(3); "   "; services(4); "    "; sv_total

LET h_total = SUM(hardware)
PRINT "  Hardware      "; hardware(1); "   "; hardware(2); "   "; hardware(3); "   "; hardware(4); "    "; h_total

LET sp_total = SUM(support)
PRINT "  Support        "; support(1); "    "; support(2); "    "; support(3); "    "; support(4); "    "; sp_total

LET grand_total = e_total + s_total + sv_total + h_total + sp_total
PRINT "  ───────────  ─────  ─────  ─────  ─────  ──────"

LET q1_total = electronics(1) + software(1) + services(1) + hardware(1) + support(1)
LET q2_total = electronics(2) + software(2) + services(2) + hardware(2) + support(2)
LET q3_total = electronics(3) + software(3) + services(3) + hardware(3) + support(3)
LET q4_total = electronics(4) + software(4) + services(4) + hardware(4) + support(4)

PRINT "  TOTAL         "; q1_total; "   "; q2_total; "   "; q3_total; "   "; q4_total; "   "; grand_total
PRINT ""

REM ─── SECTION 2: PRODUCT RANKINGS ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 2: PRODUCT LINE RANKINGS"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

DIM totals(5)
LET totals(1) = e_total
LET totals(2) = s_total
LET totals(3) = sv_total
LET totals(4) = h_total
LET totals(5) = sp_total

LET max_sales = MAX(totals)
LET bar_scale = 40

PRINT "  Revenue by Product Line"
PRINT "  ────────────────────────────────────────────────"

REM Software (highest)
LET bar_len = INT(s_total / max_sales * bar_scale)
PRINT "  Software    │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; s_total; "K"

REM Electronics
LET bar_len = INT(e_total / max_sales * bar_scale)
PRINT "  Electronics │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; e_total; "K"

REM Hardware
LET bar_len = INT(h_total / max_sales * bar_scale)
PRINT "  Hardware    │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; h_total; "K"

REM Services
LET bar_len = INT(sv_total / max_sales * bar_scale)
PRINT "  Services    │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; sv_total; "K"

REM Support
LET bar_len = INT(sp_total / max_sales * bar_scale)
PRINT "  Support     │";
FOR i = 1 TO bar_len
    PRINT "█";
NEXT i
PRINT " $"; sp_total; "K"

PRINT "  ────────────────────────────────────────────────"
PRINT ""

REM ─── SECTION 3: QUARTERLY TREND ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 3: QUARTERLY REVENUE TREND"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

DIM quarters(4)
LET quarters(1) = q1_total
LET quarters(2) = q2_total
LET quarters(3) = q3_total
LET quarters(4) = q4_total

LET q_max = MAX(quarters)

PRINT "  Total Revenue by Quarter"
PRINT "  ────────────────────────────────────────────────"

FOR q = 1 TO 4
    LET bar_len = INT(quarters(q) / q_max * bar_scale)
    PRINT "  Q"; q; "  │";
    FOR i = 1 TO bar_len
        PRINT "▓";
    NEXT i
    PRINT " $"; quarters(q); "K"
NEXT q

PRINT "  ────────────────────────────────────────────────"
PRINT ""

LET q_growth_1 = INT((q2_total - q1_total) / q1_total * 10000) / 100
LET q_growth_2 = INT((q3_total - q2_total) / q2_total * 10000) / 100
LET q_growth_3 = INT((q4_total - q3_total) / q3_total * 10000) / 100
LET annual_growth = INT((q4_total - q1_total) / q1_total * 10000) / 100

PRINT "  Quarter-over-Quarter Growth:"
PRINT "    Q1 → Q2:  +"; q_growth_1; "%"
PRINT "    Q2 → Q3:  +"; q_growth_2; "%"
PRINT "    Q3 → Q4:  +"; q_growth_3; "%"
PRINT "    Q1 → Q4:  +"; annual_growth; "% (annual)"
PRINT ""

REM ─── SECTION 4: STATISTICAL ANALYSIS ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 4: STATISTICAL ANALYSIS"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET avg_quarterly = AVG(quarters)
LET min_quarter = MIN(quarters)
LET max_quarter = MAX(quarters)

PRINT "  Quarterly Revenue Statistics:"
PRINT "    Average:   $"; INT(avg_quarterly); "K"
PRINT "    Minimum:   $"; min_quarter; "K (Q1)"
PRINT "    Maximum:   $"; max_quarter; "K (Q4)"
PRINT "    Range:     $"; max_quarter - min_quarter; "K"
PRINT ""

REM Calculate variance manually
LET variance = 0
FOR q = 1 TO 4
    LET diff = quarters(q) - avg_quarterly
    LET variance = variance + diff * diff
NEXT q
LET variance = variance / 4
LET std_dev = SQRT(variance)

PRINT "    Variance:  "; INT(variance)
PRINT "    Std Dev:   $"; INT(std_dev); "K"
PRINT ""

REM Per-product analysis
PRINT "  Per-Product Statistics:"
PRINT "  ────────────────────────────────────────"

LET e_avg = AVG(electronics)
LET e_growth = INT((electronics(4) - electronics(1)) / electronics(1) * 10000) / 100
PRINT "  Electronics: Avg $"; INT(e_avg); "K  Growth: +"; e_growth; "%"

LET s_avg = AVG(software)
LET s_growth = INT((software(4) - software(1)) / software(1) * 10000) / 100
PRINT "  Software:    Avg $"; INT(s_avg); "K  Growth: +"; s_growth; "%"

LET sv_avg = AVG(services)
LET sv_growth = INT((services(4) - services(1)) / services(1) * 10000) / 100
PRINT "  Services:    Avg $"; INT(sv_avg); "K  Growth: +"; sv_growth; "%"

LET h_avg = AVG(hardware)
LET h_growth = INT((hardware(4) - hardware(1)) / hardware(1) * 10000) / 100
IF h_growth < 0 THEN
    PRINT "  Hardware:    Avg $"; INT(h_avg); "K  Growth: "; h_growth; "%"
ELSE
    PRINT "  Hardware:    Avg $"; INT(h_avg); "K  Growth: +"; h_growth; "%"
END IF

LET sp_avg = AVG(support)
LET sp_growth = INT((support(4) - support(1)) / support(1) * 10000) / 100
PRINT "  Support:     Avg $"; INT(sp_avg); "K  Growth: +"; sp_growth; "%"
PRINT ""

REM ─── SECTION 5: MARKET SHARE ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 5: REVENUE SHARE ANALYSIS"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

LET e_share = INT(e_total / grand_total * 10000) / 100
LET s_share = INT(s_total / grand_total * 10000) / 100
LET sv_share = INT(sv_total / grand_total * 10000) / 100
LET h_share = INT(h_total / grand_total * 10000) / 100
LET sp_share = INT(sp_total / grand_total * 10000) / 100

PRINT "  Product        Revenue   Share   Contribution"
PRINT "  ───────────    ───────   ─────   ────────────"
PRINT "  Software       $"; s_total; "K   "; s_share; "%   ★ Top Performer"
PRINT "  Electronics    $"; e_total; "K   "; e_share; "%   ▲ Strong Growth"
PRINT "  Hardware       $"; h_total; "K   "; h_share; "%   ─ Stable"
PRINT "  Services       $"; sv_total; "K   "; sv_share; "%   ▲ Growing"
PRINT "  Support        $"; sp_total; "K    "; sp_share; "%   ▲ Steady"
PRINT ""

REM ─── SECTION 6: PROJECTIONS ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  SECTION 6: NEXT YEAR PROJECTIONS"
PRINT "═══════════════════════════════════════════════════"
PRINT ""

REM Simple linear projection based on growth trend
LET avg_growth = (q_growth_1 + q_growth_2 + q_growth_3) / 3
PRINT "  Average Quarterly Growth: "; INT(avg_growth * 100) / 100; "%"
PRINT ""

LET projected_q1 = INT(q4_total * (1 + avg_growth / 100))
LET projected_q2 = INT(projected_q1 * (1 + avg_growth / 100))
LET projected_q3 = INT(projected_q2 * (1 + avg_growth / 100))
LET projected_q4 = INT(projected_q3 * (1 + avg_growth / 100))
LET projected_total = projected_q1 + projected_q2 + projected_q3 + projected_q4

PRINT "  Projected FY2026 Revenue:"
PRINT "    Q1: $"; projected_q1; "K"
PRINT "    Q2: $"; projected_q2; "K"
PRINT "    Q3: $"; projected_q3; "K"
PRINT "    Q4: $"; projected_q4; "K"
PRINT "    ──────────────────"
PRINT "    Total: $"; projected_total; "K"
PRINT ""
LET yoy_growth = INT((projected_total - grand_total) / grand_total * 10000) / 100
PRINT "  ► Projected YoY Growth: +"; yoy_growth; "%"
PRINT ""

REM ─── EXECUTIVE SUMMARY ───
PRINT "═══════════════════════════════════════════════════"
PRINT "  EXECUTIVE SUMMARY"
PRINT "═══════════════════════════════════════════════════"
PRINT ""
PRINT "  Key Findings:"
PRINT "  • Total FY2025 Revenue: $"; grand_total; "K"
PRINT "  • Strongest Product: Software ($"; s_total; "K)"
PRINT "  • Fastest Growing: Services (+"; sv_growth; "%)"
PRINT "  • Revenue grew "; annual_growth; "% from Q1 to Q4"
PRINT "  • All product lines except Hardware showed"
PRINT "    consistent quarter-over-quarter growth"
PRINT ""
PRINT "  Recommendations:"
PRINT "  • Increase investment in Software and Services"
PRINT "  • Investigate Hardware declining trend"
PRINT "  • Projected FY2026 revenue: $"; projected_total; "K"
PRINT ""
PRINT "═══════════════════════════════════════════════════"
PRINT "  Sales Analytics Report Complete"
PRINT "═══════════════════════════════════════════════════"
END
