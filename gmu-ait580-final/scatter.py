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


def _calc_y_pred(df, regressand, regressor):
    x = df[regressor].values.reshape(-1, 1)
    y = df[regressand].values.reshape(-1, 1)

    reg = LinearRegression()
    model = reg.fit(x, y)
    y_pred = reg.predict(x)
    r2 = reg.score(x, y)

    return y_pred, r2


def _compute_cluster(df, regressand, regressor):
    kmeans_cluster = KMeans(n_clusters=3).fit(df[[regressor, regressand]])
    centroids = kmeans_cluster.cluster_centers_

    return kmeans_cluster, centroids


def _get_scatter(df, regressand, regressor, cluster, centroids, sns_theme="white"):

    sns.set_theme(style=sns_theme)


    fig, ax = plt.subplots(1, 1, figsize=(12, 6))

    sns.regplot(df[regressor], df[regressand], ax=ax, scatter=False)
    sns.scatterplot(
        df[regressor],
        df[regressand],
        ax=ax,
        hue=cluster.labels_,
        palette="pastel",
    )
    sns.scatterplot(
        centroids[:, 0], centroids[:, 1], ax=ax, palette="bright", s=50, color="red"
    )

    return fig


def view(data, **kwargs):

    df = data[kwargs["group_by_select_box"]]

    st.write("## Scatter & Cluster`")

    col1, col2 = st.beta_columns([1, 1])

    regressand = col1.selectbox(
        "Regress This", list(df.select_dtypes(include=np.number)), index=9
    )
    regressor = col2.selectbox(
        "On This", list(df.select_dtypes(include=np.number)), index=15
    )

    cluster, centroids = _compute_cluster(df, regressand, regressor)
    # y_pred, r2 = _calc_regression(df, regressand, regressor)
    st.pyplot(_get_scatter(df, regressand, regressor, cluster, centroids, kwargs["sns_theme"]))


    st.write('## Cluster Statistics')
    cluster_df = df.copy()
    cluster_df['cluster'] = pd.Series(cluster.labels_, index=df.index)

    cluster_df = cluster_df[['cluster', regressand]].groupby('cluster').describe().transpose()
    st.dataframe(cluster_df)
    
