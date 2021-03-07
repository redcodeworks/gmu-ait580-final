import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.regression.linear_model import RegressionResults
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
import statsmodels.api as sm

# %%


def _get_model(df, regressand, regressors):

    x = sm.add_constant(df[regressors])
    y = df[regressand]

    model = sm.OLS(y, x)
    results = model.fit()

    return results


def view(data, **kwargs):

    st.write("## Multivariate Regression Model")

    df = data[kwargs["group_by_select_box"]]

    # col1, col2 = st.beta_columns([1, 1])

    default_regressors = [
        "household_median_income",
        "median_age",
        "high_school_graduate_pct",
        "college_graduate_pct",
        "poverty_rate",
        "pop_black_pct",
        "pop_white_nonhispanic_pct",
        "pop_asian_pct",
        "pop_hispanic_latino_pct",
    ]

    regressand = st.selectbox(
        "Regress This", list(df.select_dtypes(include=np.number)), index=11
    )
    regressors = st.multiselect(
        "On These",
        list(df.select_dtypes(include=np.number)), default_regressors
    )

    if (not regressand) or (not regressors):
        st.write("Please select independent and dependent variables")
    else:
        reg_results = _get_model(df, regressand, regressors)
        st.text(reg_results.summary())
