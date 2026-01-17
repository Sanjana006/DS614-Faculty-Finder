import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from transformation.normalize_text import (
    clean_text,clean_name,
    extract_phd_field,
    validate_email,
    specialization_text_to_list,
    combine_texts,resolved_research,infer_research_from_other_fields,normalize_research,clean_publications,extract_paper_topics
)

def transform_file(input_csv,output_csv):
    df=pd.read_csv(input_csv)
    #normalizing columns
    # colums to lowercase and strip spaces
    df.columns=[c.strip().lower() for c in df.columns]
    df["name"]=df["name"].apply(clean_name)
    df['mail']=df['mail'].apply(validate_email)
    df["phd_field"] = df["phd_field"].apply(extract_phd_field)


    df["specialization"]=df["specialization"].apply(specialization_text_to_list)
    df["bio"]=df["bio"].fillna("").apply(clean_text)
    df["Research"] = df.apply(
        lambda row: resolved_research(
            row.get("Research"),
            row.get("bio"),
            row.get("specialization")
        ),
        axis=1
    )
    df["combined_text"] = df.apply(
        lambda row: combine_texts(
            row["bio"],
            row["Research"],
            row["specialization"],
            row["phd_field"]
        ),
        axis=1
    )
    df["publications"] = df["publications"].apply(clean_publications)
    # df['publications']=df['publications'].apply(extract_paper_topics)

    df.to_csv(output_csv,index=False)
    print("Transformation complete. Output saved to",output_csv)

transform_file("DS614-Faculty-Finder/transformation/dau_faculty_final.csv","transformed_faculty_data.csv")