# model.py
from sklearn.kernel_ridge import KernelRidge
from sklearn.model_selection import train_test_split, RepeatedKFold
from sklearn import metrics
import numpy as np


def train_model(df, featureset_keys, kernel="linear", alpha=1.0, gamma=None, degree=None, coef0=None):

    # Setup Parameters for Model
    kr_args = {"kernel": kernel, "alpha": alpha}

    # Validate parameters for polynomial
    if kernel == "polynomial":
        if degree is None or coef0 is None:
            print("Must provide a parameter for degree and coef0")
            return None
        else:
            kr_args["gamma"] = gamma
            kr_args["degree"] = degree
            kr_args["coef0"] = coef0

    # Initialize the figure size
    plt.figure(figsize=(20, 10))

    # Store the results of each training run
    predictions = []
    scores = []

    # Save the best model to return
    best_model = None
    baseline = 0.0

    i = 0
    for train, test in RepeatedKFold(n_splits=5, n_repeats=1).split(df):

        # Split dataset
        train_x, train_y = (df.iloc[train])[featureset_keys], (df.iloc[train])['happiness_score']
        test_x, test_y =(df.iloc[test])[featureset_keys], (df.iloc[test])['happiness_score']

        # Initialise model
        kr_model = KernelRidge(**kr_args)

        # Train model
        kr_model.fit(train_x, train_y)

        # Evaluate model
        pred_y = kr_model.predict(test_x)
        score = kr_model.score(test_x, test_y)

        # Save if better then previous
        if score > baseline:
            best_model = kr_model
        predictions.append(pred_y)
        plt.scatter(test_y, p, label=f"iter {i}")
        scores.append(score)
        i = i+1

    plt.plot(df['happiness_score'], df['happiness_score'], label='actual')
    plt.xlabel('True Values')
    plt.ylabel('Predictions')
    plt.legend(loc="upper left", bbox_to_anchor=(1.05, 1))
    return best_model, plt, scores
    print(pred_scores)

# best_model, plt, scores = train_model(cleaned_featureset, featureset_keys)
best_model, plt, scores = train_model(cleaned_featureset, featureset_keys, kernel="polynomial", degree=3, coef0=1)


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
