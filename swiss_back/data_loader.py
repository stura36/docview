import pandas as pd


def read_data(filepath):
    df_documents = pd.read_excel(filepath, sheet_name="Documents")
    df_sections = pd.read_excel(filepath, sheet_name="Sections")
    df_references = pd.read_excel(filepath, sheet_name="References")

    df_documents = preprocess_documents(df_documents)
    df_sections = preprocess_sections(df_sections)
    return df_documents, df_sections, df_references


def preprocess_documents(df):
    df["Authors"] = df.apply(lambda l: l["Authors"].split(","), axis=1)
    df = df.explode(column="Authors")
    return df


def preprocess_sections(df):
    df["DocumentID"] = df["DocumentID"].round(decimals=0).astype("int32")
    return df
