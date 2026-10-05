import os
import glob
import pandas as pd
import numpy as np

def run_sales_etl_pipeline(data_folder_path, output_filepath):
    """
    Ingests fragmented quarterly CSV files, cleans the transactional data,
    calculates financial metrics, and prepares the dataset for Power BI ingestion.
    """
    print("🚀 Starting Sales Data ETL Pipeline...")

    # 1. Consolidated Ingestion of Fragmented CSVs
    csv_files = glob.glob(os.path.join(data_folder_path, "*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in directory: {data_folder_path}")

    raw_frames = []
    for file in csv_files:
        df_temp = pd.read_csv(file)
        raw_frames.append(df_temp)
    
    df = pd.concat(raw_frames, ignore_index=True)
    print(f"✅ Ingested {len(csv_files)} quarterly reports. Total Rows: {len(df)}")

    # 2. Data Cleaning & Normalization
    df.dropna(subset=['transaction_id', 'revenue', 'units_sold'], inplace=True)
    df['date_key'] = pd.to_datetime(df['date_key'])
    df['zone'] = df['zone'].astype(str).str.strip().str.title()
    df['product_segment'] = df['product_segment'].astype(str).str.strip()

    # 3. Financial Metrics Engineering
    # Compute Revenue, Total Cost, and Margin Metrics
    df['revenue'] = df['units_sold'] * df['unit_price']
    df['total_cost'] = df['units_sold'] * df['cost_price']
    df['gross_margin'] = df['revenue'] - df['total_cost']
    
    # Avoid division by zero
    df['gross_margin_pct'] = np.where(
        df['revenue'] > 0, 
        (df['gross_margin'] / df['revenue']) * 100, 
        0
    )

    # 4. Flags & Diagnostics (Isolating South Zone Bottlenecks)
    df['is_south_zone_drag'] = np.where(
        (df['zone'] == 'South') & (df['gross_margin_pct'] < 10.0), 
        True, 
        False
    )

    # 5. Export Cleaned Dataset
    df.to_csv(output_filepath, index=False)
    print(f"🎉 Pipeline Execution Complete! Output saved to: {output_filepath}")

    # Output Quick Regional Summary
    summary = df.groupby('zone').agg(
        Total_Revenue=('revenue', 'sum'),
        Total_Margin=('gross_margin', 'sum'),
        Avg_Margin_Pct=('gross_margin_pct', 'mean')
    ).reset_index()
    
    print("\n--- Regional Performance Summary ---")
    print(summary.to_string(index=False))

if __name__ == "__main__":
    # Example execution paths
    DATA_DIR = "./raw_quarterly_csvs"
    OUTPUT_FILE = "./clean_sales_performance_data.csv"
    
    # Run pipeline (uncomment when running locally with dataset)
    # run_sales_etl_pipeline(DATA_DIR, OUTPUT_FILE)
