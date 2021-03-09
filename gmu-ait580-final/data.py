# %%
# import boto3
import io, os, json
import pandas as pd
import numpy as np
from pandas.core import base


# For reading from a secure S3 bucket with AWS credentials
# def read_csv_to_df_from_s3(object_path):

#     file_stream = io.BytesIO()

#     s3 = boto3.resource("s3", region_name="us-east-1")
#     bucket = s3.Bucket("gmu-ait580-umriley")
#     object = bucket.Object(f"{object_path}")

#     object.download_fileobj(file_stream)

#     file_stream.seek(0)

#     df = pd.read_csv(file_stream).set_index("id")

#     return df


# Reading from a hardcoded URL for grading purposes
def read_csv_to_df_from_url(file_path):
    # Ideally, this would be defined as a Docker environment variable, but this is hardcoded for grading.
    os.environ['AWS_BUCKET_URL'] = "https://gmu-ait580-umriley.s3.amazonaws.com"

    df = pd.read_csv("{}/{}".format(os.environ['AWS_BUCKET_URL'], file_path))

    return df


# Reading from a local file for debugging and development
def read_csv_to_df_from_local(file_path):

    with open(file_path, "rb") as f:
        file_stream = io.BytesIO(f.read())

    file_stream.seek(0)

    df = pd.read_csv(file_stream).set_index("id")

    return df


def _sum_columns(df, new_col, sum_cols):
    df[new_col] = df[sum_cols].sum(axis=1)

    return df


def _get_average_change(slice):

    deltas = []

    for count, col in enumerate(slice.columns):
        if count:
            old = np.array(slice[slice.columns[count - 1]])
            new = np.array(slice[slice.columns[count]])
            delta = ((new - old) / old) + 1

            deltas.append(delta)

    deltas = np.stack(deltas)


    return np.average(deltas, axis=0)


def _estimate_year(
    df, base_col_name, years=[2005, 2006, 2007], est_year=2010, drop_original=True
):

    last_year = f"{base_col_name}_{years[-1]}"
    atts = [f"{base_col_name}_{str(year)}" for year in years]

    avg_change = _get_average_change(df[atts])
    periods = est_year - years[-1]
    multiplier = avg_change ** periods

    df[base_col_name] = df[last_year] * multiplier

    # Replace invalid calculations with nan and drop the nans
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    df[base_col_name] = df[base_col_name].astype("int")

    if drop_original:
        df.drop(atts, inplace=True, axis=1)

    return df


def _normalize_per_capita(df, base_col, norm_col, drop_original=True):
    df[f"{base_col}_pct"] = round((df[base_col] * 100) / df[norm_col], 2)

    if drop_original:
        df.drop([base_col], inplace=True, axis=1)

    return df


def _order_cols(df, col_order):
    return df[col_order]


def _get_df(path, data_cleaning_list):
    print(f"\nGenerating dataframe from {path}")
    # read_csv_to_df = read_csv_to_df_from_local
    # read_csv_to_df = read_csv_to_df_from_s3
    read_csv_to_df = read_csv_to_df_from_url

    df = read_csv_to_df(path)

    df.replace([np.inf, -np.inf, 0], np.nan, inplace=True)
    df.dropna(inplace=True)

    for col_name in data_cleaning_list["estimate"]:
        print(f"Estimating {col_name}")
        df = _estimate_year(df, col_name)

    for new_col in data_cleaning_list["sum"]:
        print(f"Caculculating {new_col}")
        df = _sum_columns(df, new_col, data_cleaning_list["sum"][new_col])

    for norm_name in data_cleaning_list["normalize"]:
        for col_name in data_cleaning_list["normalize"][norm_name]:
            print(f"Normalizing {col_name} to {norm_name}")
            df = _normalize_per_capita(df, col_name, norm_name)

    # print(f"Dropping unneeded columns {data_cleaning_list['unneeded']}")
    # df.drop(data_cleaning_list['unneeded'], inplace=True, axis=1)

    print("Ordering and dropping columns")
    df = _order_cols(df, data_cleaning_list["order"])

    print("Done with data cleaning")

    return df


def _get_corr_matrix(df):
    return df.corr()


def get_data():

    # !Important! This maps which columns should receive which cleaning functions
    with open("data_cleaning.json", "r") as f:
        data_cleaning_list = json.load(f)

    counties_df = _get_df("counties.csv", data_cleaning_list)
    counties_corr = _get_corr_matrix(counties_df)
    states_df = _get_df("states.csv", data_cleaning_list)
    states_corr = _get_corr_matrix(states_df)

    data = {
        "Counties": counties_df,
        "Counties_Corr": counties_corr,
        "States": states_df,
        "States_Corr": states_corr,
    }

    return data


data = get_data()
states_df = data["States"]
counties_df = data["Counties"]

# %%
states_df.columns

# %%
states_df.head()
# %%
