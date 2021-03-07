import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

# %%


def _get_corr_map(corr, sns_theme="white"):

    sns.set_theme(style=sns_theme)

    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(1, 1, figsize=(12, 12))

    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    ax = sns.heatmap(
        corr,
        mask=mask,
        cmap=cmap,
        vmax=0.3,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
    )

    return fig


def _get_corr_df(corr_matrix, atts):

    if atts:
        return corr_matrix[atts].sort_values(atts, ascending=False)

    else:
        return corr_matrix


def view(data, **kwargs):

    st.write("## Correlation")

    df = data[kwargs["group_by_select_box"]]
    corr = data[f"{kwargs['group_by_select_box']}_Corr"]

    st.pyplot(_get_corr_map(corr))

    corr_atts = st.multiselect(
        "Correlation Attributes",
        list(df.select_dtypes(include=np.number)),
        ["insured_18_to_65_pct", "insured_under_18_pct"],
    )

    st.dataframe(_get_corr_df(corr, corr_atts))


# %%
# states = st.multiselect("Choose states", list(states_df['state']), ['CALIFORNIA'])

# data = states_df[states_df['state'].isin(states)]
# st.write("### Population", data.sort_index())

# pop_fig = get_pop_fig(data)
# st.pyplot(pop_fig)