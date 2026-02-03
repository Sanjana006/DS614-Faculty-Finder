"""
This module defines the transformation pipeline for faculty data.
It reads the raw CSV file, applies normalization functions to relevant columns,
and saves the transformed data to a new CSV file.
"""

import sys
import os
import pandas as pd

# --------------------------------------------------
# Ensure project root is in Python path
# --------------------------------------------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.settings import RAW_DATA_PATH, CLEANED_DATA_PATH
from transformation.normalize_text import (
    clean_text,
    clean_name,
    validate_email,
    specialization_text_to_list,
    combine_texts,
    normalize_research,
    clean_publication
)

# --------------------------------------------------
# Utility: Add faculty_id column
# --------------------------------------------------
def add_faculty_id_df(df: pd.DataFrame, prefix: str = "DAU") -> pd.DataFrame:
    df_out = df.copy()

    if "faculty_id" not in df_out.columns:
        df_out.insert(
            0,
            "faculty_id",
            [f"{prefix}{str(i).zfill(3)}" for i in range(1, len(df_out) + 1)]
        )

    return df_out

# --------------------------------------------------
# Main Transformation Function
# --------------------------------------------------
def transform_file(input_csv: str, output_csv: str) -> None:
    df = pd.read_csv(input_csv)

    # Normalize column names
    df.columns = [c.strip().lower() for c in df.columns]

    # Apply transformations
    df["name"] = df["name"].apply(clean_name)
    df["mail"] = df["mail"].apply(validate_email)
    df["specialization"] = df["specialization"].apply(specialization_text_to_list)
    df["bio"] = df["bio"].fillna("").apply(clean_text)
    df["research"] = df.apply(normalize_research, axis=1)

    df["combined_text"] = df.apply(
        lambda row: combine_texts(
            row["bio"],
            row["research"],
            row["specialization"],
            row["phd_field"]
        ),
        axis=1
    )

    df["publications"] = df["publications"].apply(clean_publication)

    # Add faculty ID
    df = add_faculty_id_df(df, prefix="DAU")

    # Save transformed data
    df.to_csv(output_csv, index=False)
    print(f"Transformation complete. Output saved to {output_csv}")

# --------------------------------------------------
# Execute transformation
# --------------------------------------------------
if __name__ == "__main__":
    transform_file(RAW_DATA_PATH, CLEANED_DATA_PATH)
