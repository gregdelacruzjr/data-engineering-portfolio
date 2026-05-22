from google.cloud import bigquery
import pandas as pd

# Google Cloud project and dataset details
# Project: https://console.cloud.google.com
PROJECT_ID = "project-cf86832b-05ad-4453-847"
DATASET_ID = "data_engineering_portfolio"
TABLE_ID = "ph_population"

# Full table reference
TABLE_REF = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

def load_csv_to_bigquery(filepath):
    """Load a CSV file into a BigQuery table."""
    
    # Initialize BigQuery client — uses ADC automatically
    client = bigquery.Client(project=PROJECT_ID)
    
    # Load CSV into pandas DataFrame first
    df = pd.read_csv(filepath)
    print(f"✓ CSV loaded — {len(df)} rows, {len(df.columns)} columns")
    print(df)
    
    # Define load job configuration
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    
    # Load DataFrame into BigQuery
    job = client.load_table_from_dataframe(df, TABLE_REF, job_config=job_config)
    job.result()  # Wait for job to complete
    
    print(f"\n✓ Data loaded into BigQuery table: {TABLE_REF}")
    print(f"✓ {len(df)} rows written successfully")

def main():
    print("Loading Population Data to BigQuery")
    print("=" * 40)
    load_csv_to_bigquery("notes/population_clean.csv")

if __name__ == "__main__":
    main()