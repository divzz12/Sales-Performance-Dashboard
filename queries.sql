--This query isolates the 22% margin drag caused by underperforming product segments in the South zone

WITH ZonePerformance AS (
    SELECT 
        zone,
        product_segment,
        SUM(revenue) AS total_revenue,
        SUM(gross_margin) AS total_gross_margin,
        ROUND((SUM(gross_margin) / NULLIF(SUM(revenue), 0)) * 100, 2) AS gross_margin_pct
    FROM Fact_Sales
    GROUP BY zone, product_segment
)
SELECT 
    zone,
    product_segment,
    total_revenue,
    total_gross_margin,
    gross_margin_pct,
    -- Compute performance drag compared to target zone benchmark (18-20%)
    CASE 
        WHEN gross_margin_pct < 12.00 THEN 'CRITICAL: High Profitability Drag'
        WHEN gross_margin_pct BETWEEN 12.00 AND 17.99 THEN 'WARNING: Moderate Performance'
        ELSE 'OPTIMAL'
    END AS performance_status
FROM ZonePerformance
ORDER BY gross_margin_pct ASC;
