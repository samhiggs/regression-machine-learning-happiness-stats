import numpy as np
import pandas as pd

def clean_dataset(data):
    #Select the quantatitive columns. We are ignoring categorical data for this analysis
    cleaned_featureset = data.select_dtypes(include=['int64', 'float64'])

    #Remove happiness_rank and happiness_score
    cleaned_featureset = cleaned_featureset.drop(
        columns=['happiness_rank', 'happiness_score'])

    #Convert 0's to NAN as there shouldn't be 0's in this dataset unless the value couldn't be calculated
    cleaned_featureset = cleaned_featureset.replace(0.0, np.NaN)

    #Replace the NA's with mean of column to keep consistent length
    cleaned_featureset = cleaned_featureset.apply(lambda x: x.fillna(x.mean()),axis=0)

    #Add constant to columns with negative values so that all are positive
    cleaned_featureset = cleaned_featureset.apply(
        lambda x: x.sub(x.min()-1) if x.min() < 0 else x)

    #Transform columns which have significant outliers and skewed data
    #Chose not to remove outliers as their information could still be significant
    transform_cube_cols = ['cellular_subscriptions', 'familiy_income_gini_coeff']
    transform_log_cols=['military_expenditures[%]', 'population', 'GDP_per_capita[$]',
    'inflation_rate[%]']

    cleaned_featureset[transform_cube_cols] = cleaned_featureset[
        transform_cube_cols].apply(lambda x: x.transform(np.cbrt))

    cleaned_featureset[transform_log_cols] = cleaned_featureset[
        transform_log_cols].apply(lambda x: x.transform(np.log))
    cleaned_featureset['surplus_deficit_GDP[%]'] = \
        cleaned_featureset['surplus_deficit_GDP[%]'].pow(3)
    #normalize data to fit between 0 and 1
    cleaned_featureset = cleaned_featureset.apply(
        lambda x: [(el-x.min())/(x.max()-x.min()) for el in x], axis=0)

    cleaned_featureset.insert(0, 'happiness_score', data['happiness_score'])
    return cleaned_featureset