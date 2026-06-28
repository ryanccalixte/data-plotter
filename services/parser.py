from io import BytesIO

import pandas as pd


def cleandata(formcontent):
    # read the uploaded data file and remove unusable columns
    uploaded_file = formcontent["file"]
    filename = (uploaded_file.filename or "").lower()
    file_bytes = uploaded_file.file.read()

    if filename.endswith(".csv"):
        filedata = pd.read_csv(BytesIO(file_bytes))
    elif filename.endswith(".tsv") or filename.endswith(".txt"):
        filedata = pd.read_csv(BytesIO(file_bytes), sep="\t")
    elif filename.endswith(".json"):
        filedata = pd.read_json(BytesIO(file_bytes))
    elif filename.endswith(".xlsx"):
        filedata = pd.read_excel(BytesIO(file_bytes))
    else:
        raise ValueError("unsupported file type, please upload csv, json, xlsx, tsv, or txt")

    # remove columns that contain missing values
    cols_withmissing = [col for col in filedata.columns if filedata[col].isnull().any()]
    filedata = filedata.drop(columns=cols_withmissing)

    # remove columns that store text values
    string_cols = filedata.select_dtypes(include="object").columns
    filedata.drop(columns=string_cols, inplace=True)

    return filedata