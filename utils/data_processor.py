"""Data processing utilities."""
import pandas as pd
import io
from typing import Tuple, Optional


def process_load_csv(csv_file) -> Tuple[pd.DataFrame, str]:
    """
    Process uploaded load CSV.

    Expected columns: timestamp, load_kw
    """
    try:
        df = pd.read_csv(csv_file)

        # Validate columns
        if "load_kw" not in df.columns:
            return None, "❌ CSV must contain 'load_kw' column"

        # Try to parse timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            if df["timestamp"].isna().any():
                return None, "❌ Some timestamps could not be parsed"

        # Validate load values
        if df["load_kw"].isna().any():
            return None, "❌ Some load_kw values are missing"

        if (df["load_kw"] < 0).any():
            return None, "❌ load_kw values must be non-negative"

        return df, "✓ Load data valid"

    except Exception as e:
        return None, f"❌ Error processing CSV: {str(e)}"


def process_pv_csv(csv_file) -> Tuple[pd.DataFrame, str]:
    """
    Process uploaded PV generation CSV.

    Expected columns: timestamp, pv_kw
    """
    try:
        df = pd.read_csv(csv_file)

        # Validate columns
        if "pv_kw" not in df.columns:
            return None, "❌ CSV must contain 'pv_kw' column"

        # Try to parse timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            if df["timestamp"].isna().any():
                return None, "❌ Some timestamps could not be parsed"

        # Validate PV values
        if df["pv_kw"].isna().any():
            return None, "❌ Some pv_kw values are missing"

        if (df["pv_kw"] < 0).any():
            return None, "❌ pv_kw values must be non-negative"

        return df, "✓ PV data valid"

    except Exception as e:
        return None, f"❌ Error processing CSV: {str(e)}"


def load_demo_data(data_dir: str = "data") -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load demo load and PV CSV files."""
    try:
        load_df = pd.read_csv(f"{data_dir}/demo_load.csv")
        pv_df = pd.read_csv(f"{data_dir}/demo_pv.csv")

        load_df["timestamp"] = pd.to_datetime(load_df["timestamp"])
        pv_df["timestamp"] = pd.to_datetime(pv_df["timestamp"])

        return load_df, pv_df
    except Exception as e:
        raise Exception(f"Failed to load demo data: {str(e)}")


def align_timeseries(load_df: pd.DataFrame, pv_df: pd.DataFrame) -> Tuple[pd.Series, pd.Series]:
    """Align load and PV timeseries by timestamp."""
    # Merge on timestamp
    merged = pd.merge(load_df, pv_df, on="timestamp", how="inner")

    if len(merged) == 0:
        raise ValueError("No matching timestamps between load and PV data")

    return merged["load_kw"], merged["pv_kw"]
