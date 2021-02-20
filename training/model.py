# model.py
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split, RepeatedKFold
from sklearn import metrics
import numpy as np


def train(cleaned_featureset):
    """
    Training a Kernel Ridge Regression model
    """
    featureset_keys = ['economy', 'family', 'health',
                   'freedom', 'dystopia_residual',
                   'internet_access_population[%]',
                   'cellular_subscriptions', 'GDP_per_capita[$]',
                   'inflation_rate[%]'
                  ]
    featureset = cleaned_featureset[featureset_keys]
    rkf = RepeatedKFold(n_splits=5, n_repeats=1)
    iteration = 0
    pred_list = []
    pred_val_list = []
    best_model = None
    baseline = -1
    for train, test in rkf.split(cleaned_featureset):
        train_x, train_y = (cleaned_featureset.iloc[train])[featureset_keys], (cleaned_featureset.iloc[train])['happiness_score']
        test_x, test_y =(cleaned_featureset.iloc[test])[featureset_keys], (cleaned_featureset.iloc[test])['happiness_score']
        #Create model
        clf = KernelRidge(alpha=1)
        #Build model with training data
        fit = clf.fit(train_x, train_y)
        #now use the model to
        pred_y = clf.predict(test_x)
        score = clf.score(test_x, test_y)
        if score > baseline:
            best_model = clf
        pred_list.append(pred_y)
        pred_val_list.append(score)


if __name__ == '__main__':

    iris_data = datasets.load_iris()
    X = iris_data['data']
    y = iris_data['target']

    labels = {
        0: 'iris-setosa',
        1: 'iris-versicolor',
        2: 'iris-virginica'
    }

    # rename integer labels to actual flower names
    y = np.vectorize(labels.__getitem__)(y)

    mdl = train(X, y)

    # serialize model
    joblib.dump(mdl, 'iris.mdl')
