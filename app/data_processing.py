import pandas as pd

def load_data(csv_path):
    """Loads and preprocesses agricultural data from CSV."""
    df = pd.read_csv(csv_path)
    
    df["DISTRICT_NAME"] = df["DISTRICT_NAME"].str.upper().str.strip()
    df["DISTRICT_CODE"] = df["DISTRICT_CODE"].astype(str).str.zfill(2)
    
    # Extract crop names and year columns
    df_long = pd.melt(df, id_vars=["DISTRICT_CODE", "DISTRICT_NAME"], var_name="Variable", value_name="Value")
    df_long["Crop"] = df_long["Variable"].str.split('_').str[0]  # Extract crop abbreviation
    df_long["Metric"] = df_long["Variable"].str.split('_').str[1]  # Extract metric (Y, P, A)
    df_long["Year"] = df_long["Variable"].str.extract(r'(\d{6})')
    
    # Pivot table to separate Yield, Production, and Area
    df_processed = df_long.pivot_table(index=["DISTRICT_CODE", "DISTRICT_NAME", "Crop", "Year"], 
                                       columns="Metric", values="Value", aggfunc="first").reset_index()
    df_processed.columns.name = None  # Remove the column name hierarchy
    df_processed.rename(columns={"Y": "Yield", "P": "Production", "A": "Area"}, inplace=True)
    
    return df_processed