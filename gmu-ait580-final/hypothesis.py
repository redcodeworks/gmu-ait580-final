from scipy.stats.stats import ttest_ind
import seaborn as sns
from scipy import stats
import streamlit as st
import numpy as np

def ttest_ind(a, b, alpha, alternative):
    t2, p2 = stats.ttest_ind(a ,b, alternative=alternative)

    st.write("#####")
    col1, col2 = st.beta_columns([1, 1])

    col1.text(f"Two sample T-Test, {alternative}")
    col2.text("Alpha = {}".format(alpha))
    col1.text("T = {}".format(t2))
    col2.text("P = {}".format(p2))

    if alternative == "two":
        alpha = alpha / 2
        reject_h0 = p2 < alpha

    else:
        reject_h0 = p2 < alpha

    if reject_h0:
        st.text("Reject the null hypothesis.")

    else:
        st.text("Fail to reject the null hypothesis.")

    st.write("####")


def setup_hypothesis(desc, df, sample_att, mean_att, pivot_value, alternative):
    
    equality = {'less': ['>=', '<'] , 'greater': ['<=', '>'], 'two-sided': ['', '']}
    qualifier = {'less': ['greater than or equal to', 'less than'] , 'greater': ['less than or equal to', 'greater than'], 'two-sided': ['equal to', 'different from']}


    st.write(f"##### H0: {desc} '{equality[alternative][0]}{pivot_value}' has a mean {qualifier[alternative][0]} the mean of the other counties.")
    st.write(f"##### HA: {desc} '{equality[alternative][1]}{pivot_value}' has a mean {qualifier[alternative][1]} the mean of the other counties.")

    a = df[df[sample_att] > pivot_value][mean_att]
    b = df[df[sample_att] <= pivot_value][mean_att]

    return a, b

def view(data, **kwargs):

    df = data[kwargs["group_by_select_box"]]


    st.write('## Hypothesis Tests')

    col1, col2 = st.beta_columns([1, 1])
    alpha = float(col1.text_input("Significance Level", 0.05))
    sample_att = col2.selectbox("Sample Attribute", list(df.select_dtypes(include=np.number)), index=11)

    st.write("---")
    
    st.write('## Economic')

    st.write("#### Houshold Median Income")
    median_income_h = int(st.text_input("Household Median Income", 58000))
    a, b = setup_hypothesis("Houshold Median Income", df, 'household_median_income', 'insured_pct', median_income_h, "greater")
    ttest_ind(a, b, alpha, "greater")

    st.write("#### Wages as a proportion of income")
    wages_prop_h = int(st.text_input("Wages as a proportion of income", 90))
    a, b = setup_hypothesis("Wages as a proportion of income", df, 'irs_wages_pct', 'insured_pct', wages_prop_h, "two-sided")
    ttest_ind(a, b, alpha, "two-sided")

    st.write("#### Poverty")
    poverty_rate_h = int(st.text_input("Poverty Rate", 12))
    a, b = setup_hypothesis("Poverty Rate", df, 'poverty_rate', 'insured_pct', poverty_rate_h, "less")
    ttest_ind(a, b, alpha, "less")

    
    st.write("---")
    st.write("## Education")
    st.write("### High School Graduation")
    hs_graduation_rate = int(st.text_input("High School Graduation Rate", 80))
    a, b = setup_hypothesis("High School Graduation rate", df, 'high_school_graduate_pct', 'insured_pct', hs_graduation_rate, "greater")
    ttest_ind(a, b, alpha, "greater")


    st.write("### College Graduation")
    college_graduation_rate = int(st.text_input("College Graduation Rate", 20))
    a, b = setup_hypothesis("College Graduation rate", df, 'college_graduate_pct', 'insured_pct', college_graduation_rate, "greater")
    ttest_ind(a, b, alpha, "greater")


    st.write("---")
    st.write("## Race")

    st.write("### White Non-Hispanic")
    wnh_pct = int(st.text_input("White Non-Hispanic", 75))
    a, b = setup_hypothesis("White Non-Hispanic", df, 'pop_white_nonhispanic_pct', 'insured_pct', wnh_pct, "greater")
    ttest_ind(a, b, alpha, "greater")

    st.write("### Black")
    blk_pct = int(st.text_input("Black", 75))
    a, b = setup_hypothesis("Black", df, 'pop_black_pct', 'insured_pct', blk_pct, "less")
    ttest_ind(a, b, alpha, "less")

    st.write("### Asian")
    asn_pct = int(st.text_input("Asian", 12))
    a, b = setup_hypothesis("Asian", df, 'pop_asian_pct', 'insured_pct', asn_pct, "two-sided")
    ttest_ind(a, b, alpha, "two-sided")

    st.write("### Hispanic")
    hsp_pct = int(st.text_input("Hispanic", 30))
    a, b = setup_hypothesis("Hispanic", df, 'pop_hispanic_latino_pct', 'insured_pct', hsp_pct, "less")
    ttest_ind(a, b, alpha, "less")


