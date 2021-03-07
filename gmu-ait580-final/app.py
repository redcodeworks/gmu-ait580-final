# %%
import streamlit as st

# st.set_page_config(layout="wide")

from data import get_data
import exploration, correlation, scatter, hypothesis, regression


# %%
@st.cache
def get_dfs():
    return get_data()


def get_views():
    return {
        "Data Explorer": exploration,
        "Correlation": correlation,
        "Hypothesis Tests": hypothesis,
        "Scatter": scatter,
        "Regression Analysis": regression,
    }


data = get_dfs()
views = get_views()

# %%
st.title("Health Insurance and Population Demographics By County")


analysis_selectbox = st.sidebar.selectbox(
    "Select an analysis", list(views.keys()), index=0
)

group_by_select_box = st.sidebar.selectbox("Group By", ["States", "Counties"], index=1)

sns_theme = st.sidebar.radio(
    "Chart Themes", ["whitegrid", "white", "dark", "darkgrid", "ticks"], index=3
)


page = views[analysis_selectbox]

page.view(data, group_by_select_box=group_by_select_box, sns_theme=sns_theme)
