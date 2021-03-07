import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st


def _get_quantile_filtered_df(df, att, qnt_filter=(0, 100)):
    return df[
        (df[att] >= df[att].quantile(qnt_filter[0] / 100))
        & (df[att] <= df[att].quantile(qnt_filter[1] / 100))
    ]


def _get_hist_fig(df, att, sns_theme="whitegrid"):
    sns.set_theme(style=sns_theme)

    fig, ax = plt.subplots(1, 1, figsize=(8, 6))

    mean = df[att].mean()
    median = df[att].median()

    ax = sns.histplot(data=df, x=att)
    ax.axvline(mean, color="red", linestyle="--")
    ax.axvline(median, color="orange", linestyle="--")
    plt.legend({"Mean": mean, "Median": median})
    ax.set(title="Histogram")

    return fig


def _get_boxplot_fig(df, att, sns_theme="whitegrid"):
    sns.set_theme(style=sns_theme)

    fig, ax = plt.subplots(1, 1, figsize=(8, 1))

    ax = sns.boxplot(data=df, x=att, showmeans=True)
    ax.set(title="Boxplot")

    return fig


def _get_top_10_df(df, att, ascending=False):
    return (
        df[["desc", "abb", att]]
        .sort_values(att, ascending=ascending)
        .set_index("abb")
        .head(10)
    )


def view(data, **kwargs):

    st.write("## Data Explorer")

    df = data[kwargs["group_by_select_box"]]

    att = st.selectbox(
        "Choose an attribute", list(df.select_dtypes(include=np.number)), index=10
    )

    percentile_to_filter = st.slider("Percentile", 0, 100, (0, 100))
    filtered_qnt_df = _get_quantile_filtered_df(
        df, att, qnt_filter=percentile_to_filter
    )

    st.write("### Distribution")
    st.pyplot(_get_hist_fig(filtered_qnt_df, att, kwargs["sns_theme"]))
    st.pyplot(_get_boxplot_fig(filtered_qnt_df, att, kwargs["sns_theme"]))

    st.write("---")
    col1, col2 = st.beta_columns([1, 2])
    col1.write("### Summary Stats")

    col1.write("#### Descriptive Statistics")
    col1.dataframe(filtered_qnt_df[att].describe())

    ascending = col2.checkbox("Show Bottom 10", False)
    col2.write("#### Top 10")
    col2.dataframe(_get_top_10_df(filtered_qnt_df, att, ascending))

    st.write("---")
    st.write("### Dataset")
    col1, col2 = st.beta_columns([1, 1])
    atts = st.multiselect("Choose Attributes", list(df.select_dtypes(include=np.number)), ["uninsured_under_18_pct", "uninsured_18_to_65_pct"],
    )
    items = st.multiselect("Choose Items", list(df['desc']))

    if items:
        st.dataframe(filtered_qnt_df[['desc'] + atts][df["desc"].isin(items)].set_index("desc"))
    else:
        st.dataframe(filtered_qnt_df[['desc'] + atts].set_index("desc"))


# %%
# states = st.multiselect("Choose states", list(states_df['state']), ['CALIFORNIA'])

# data = states_df[states_df['state'].isin(states)]
# st.write("### Population", data.sort_index())

# pop_fig = get_pop_fig(data)
# st.pyplot(pop_fig)