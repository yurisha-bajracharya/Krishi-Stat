import pandas as pd
import matplotlib.pyplot as plt

def load_data(csv_path):
    """Loads and preprocesses agricultural data from CSV."""
    df = pd.read_csv(csv_path)
    
    df["DISTRICT_NAME"] = df["DISTRICT_NAME"].str.upper().str.strip()
    df["DISTRICT_CODE"] = df["DISTRICT_CODE"].astype(str).str.zfill(2)

    # Extract year columns
    yield_cols = [col for col in df.columns if "_Y_" in col]
    prod_cols = [col for col in df.columns if "_P_" in col]
    area_cols = [col for col in df.columns if "_A_" in col]
    
    df_yield = df.melt(id_vars=["DISTRICT_CODE", "DISTRICT_NAME"], 
                        value_vars=yield_cols, 
                        var_name="Year", value_name="Yield")
    df_yield["Year"] = df_yield["Year"].str.extract(r'(\d{6})')

    df_prod = df.melt(id_vars=["DISTRICT_CODE", "DISTRICT_NAME"], 
                       value_vars=prod_cols, 
                       var_name="Year", value_name="Production")
    df_prod["Year"] = df_prod["Year"].str.extract(r'(\d{6})')

    df_area = df.melt(id_vars=["DISTRICT_CODE", "DISTRICT_NAME"], 
                       value_vars=area_cols, 
                       var_name="Year", value_name="Area")
    df_area["Year"] = df_area["Year"].str.extract(r'(\d{6})')

    # Merge all
    df_merged = df_yield.merge(df_prod, on=["DISTRICT_CODE", "DISTRICT_NAME", "Year"])
    df_merged = df_merged.merge(df_area, on=["DISTRICT_CODE", "DISTRICT_NAME", "Year"])

    return df_merged