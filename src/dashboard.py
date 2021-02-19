import streamlit as st
import requests
import pandas as pd

import plotly.express as px
import plotly.graph_objs as go

from clean import clean_dataset

st.title("Word Happiness Indicator")
st.subheader("Investigating how nations indicators affect happiness using machine learning regression techniques")

# Example of how to hit the API
def score(data):
    req = requests.get("http://0.0.0.0:9696/test")
    return req.text

# Sidebar
def generate_sidebar():
    pass

def generate_main():
    data = pd.read_csv('data/happiness.csv', delimiter=',', header=0, skip_blank_lines=False)
    st.dataframe(data)
    cleaned_featureset = clean_dataset(data)
    st.dataframe(cleaned_featureset.describe().T)

    feature = st.selectbox("Select a feature to compare with Happiness", cleaned_featureset.columns)
    fig = px.scatter(cleaned_featureset, x=feature, y="happiness_score")
    st.plotly_chart(fig)
    corr = cleaned_featureset.corr()

    heatmap_fig = go.Figure(
        data = go.Heatmap(
            z=corr.values,
            x=corr.index.values,
            y=corr.columns.values))

    st.plotly_chart(heatmap_fig)

if __name__ == "__main__":
    generate_sidebar()
    generate_main()