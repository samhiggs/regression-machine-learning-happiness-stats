import streamlit as st
import requests
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

from clean import clean_dataset


@st.cache()
def read_data():
    data = pd.read_csv('data/happiness.csv', delimiter=',', header=0, skip_blank_lines=False)
    return clean_dataset(data)


st.title("Word Happiness Indicator")
st.subheader("Investigating how nations indicators affect happiness using machine learning regression techniques")


def score(data):
    req = requests.post("http://0.0.0.0:9696/score", json=data)
    return req.json()


def filter_dict(dict):
    keys = [
        'freedom', 'dystopia_residual', 'internet_access_population[%]',
        'cellular_subscriptions', 'familiy_income_gini_coeff', 'GDP_per_capita[$]',
        'inflation_rate[%]', 'military_expenditures[%]', 'population'
    ]
    return {k : dict[k] for k in keys}


def generate_sidebar(cleaned_featureset):
    '''
    Sidebar
    '''
    st.sidebar.subheader("Create your own Happiness")
    user_vals = {k : None for k in cleaned_featureset.columns[1:]}
    for col in cleaned_featureset.columns[1:]:
        user_vals[col] = round(st.sidebar.slider(
            col,
            min_value=min(cleaned_featureset[col]),
            max_value=max(cleaned_featureset[col]),
            value=sum(cleaned_featureset[col])/len(cleaned_featureset[col])), 3)
    st.sidebar.subheader("Payload sent to model")
    st.sidebar.write(user_vals)
    run_prediction = st.sidebar.button("Predict")

    if run_prediction:
        score_val = score(filter_dict(user_vals))
        st.sidebar.write(f"Prediction: {score_val['score']}")


def generate_main(cleaned_featureset):

    st.dataframe(cleaned_featureset.describe().T)

    feature = st.selectbox("Select a feature to compare with Happiness", cleaned_featureset.columns)
    fig = px.scatter(cleaned_featureset, x=feature, y="happiness_score")
    st.plotly_chart(fig)
    corr = cleaned_featureset.corr()

    heatmap_fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.index.values,
            y=corr.columns.values))

    heatmap_fig.update_layout(
        height=700,
        width=700
    )
    st.plotly_chart(heatmap_fig)


if __name__ == "__main__":

    cleaned_featureset = read_data()
    generate_sidebar(cleaned_featureset)
    generate_main(cleaned_featureset)