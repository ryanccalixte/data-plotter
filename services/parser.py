import pandas as pd


def cleandata(formcontent):
    filedata = pd.read_csv(formcontent['file'].file)

    # Drops columns with missing data
    cols_withmissing = [col for col in filedata.columns if filedata[col].isnull().any()]
    filedata = filedata.drop(columns=cols_withmissing)

    # Drops columns with string data
    string_cols = filedata.select_dtypes(include='object').columns
    filedata.drop(columns=string_cols, inplace=True)
        
        

    return filedata