'''
in this module we define the transformation pipeline for faculty data
we read the raw csv file, apply normalization functions to relevant columns,
and save the transformed data to a new csv file.
'''


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from transformation.normalize_text import (
    clean_text,clean_name,
    validate_email,
    specialization_text_to_list,
    combine_texts,normalize_research,clean_publication
)

## this function adds faculty_id column to dataframe
def add_faculty_id_df(df: pd.DataFrame, prefix: str = "DAU") -> pd.DataFrame:
    df_out = df.copy()

    if "faculty_id" not in df_out.columns:
        df_out.insert(
            0,
            "faculty_id",
            [f"{prefix}{str(i).zfill(3)}" for i in range(1, len(df_out) + 1)]
        )

    return df_out

def transform_file(input_csv,output_csv):
    df=pd.read_csv(input_csv,)
    #normalizing columns
    # colums to lowercase and strip spaces
    df.columns=[c.strip().lower() for c in df.columns]
    df["name"]=df["name"].apply(clean_name)
    df['mail']=df['mail'].apply(validate_email)
    df["specialization"]=df["specialization"].apply(specialization_text_to_list)
    df["bio"]=df["bio"].fillna("").apply(clean_text)
    df["research"] = df.apply(normalize_research)
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
    df=add_faculty_id_df(df,prefix="DAU")

    df.to_csv(output_csv,index=False)
    print("Transformation complete. Output saved to",output_csv)


