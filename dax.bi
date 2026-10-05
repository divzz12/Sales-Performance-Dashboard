// Total Revenue Metric
Total Revenue = SUM(Fact_Sales[revenue])

// Month-over-Month (MoM) Revenue Growth %
MoM Revenue Growth % = 
VAR CurrentMonth = [Total Revenue]
VAR PriorMonth = CALCULATE([Total Revenue], DATEADD('Dim_Date'[Date], -1, MONTH))
RETURN
DIVIDE(CurrentMonth - PriorMonth, PriorMonth, 0) * 100

// Gross Margin Drag Benchmark (South Zone)
South Zone Margin Drag % = 
VAR BenchmarkMargin = 0.20 -- Target 20% Gross Margin
VAR ActualSouthMargin = DIVIDE(
    CALCULATE(SUM(Fact_Sales[gross_margin]), Fact_Sales[zone] = "South"),
    CALCULATE(SUM(Fact_Sales[revenue]), Fact_Sales[zone] = "South"),
    0
)
RETURN
BenchmarkMargin - ActualSouthMargin
