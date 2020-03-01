"""
An example of using Python's built in `multiprocessing` or `discomp`
to test many hyperparameters.

To test 30 hyperparameter configurations on my MacBook Pro it took:
* 81 minutes and 30 seconds using `map`
* 34 minutes and 40 seconds using `multiprocessing.Pool().map`
* 8 minutes and 52 seconds using `discomp.Pool().map`

More background at https://dis.co/blog/machine-learning-with-disco/
"""

import os
import random
import multiprocessing

import numpy as np
import xgboost
from sklearn.model_selection import train_test_split
from sklearn import metrics

import pandas as pd
import discomp


os.environ["DISCO_LOGIN_USER"] = "your-email-or-use-environment-variables"
os.environ["DISCO_LOGIN_PASSWORD"] = "your-password-or-api-key"

print("loading data")
url = "https://discodemo.s3-us-west-2.amazonaws.com/yuval/creditcard.csv"
df = pd.read_csv(url, header=0)


def test_fit(params):
    # This function will be launched multiple times in other processes
    Y = df["Class"]
    X = df.drop(["Class"], axis=1)
    print("Dataset X shape: {}".format(X.shape))
    print("Dataset Y shape: {}".format(Y.shape))
    print("{}\n\n{}".format(X[:2], Y[:2]))

    # split data into train and test sets
    seed = 7
    test_size = 0.33
    X_train, X_test, y_train, y_test = train_test_split(
        X, Y, test_size=test_size, random_state=seed
    )

    print("fit model")
    model = xgboost.XGBRegressor(objective="reg:squarederror", **params)
    model.fit(X_train, y_train)

    # make predictions for test data
    print("predict")
    y_pred = model.predict(X_test)

    print("evaluating predictions")
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred)
    roc_auc = metrics.auc(fpr, tpr)

    print(f"roc_auc: {roc_auc:.2} params: {params}")
    return roc_auc


# Set up a random search through hyper parameters
param_options = []
param_test_count = 30
for i in range(param_test_count):
    params = dict(
        max_depth=random.randint(2, 100),
        num_boost_round=random.randint(2, 1000),
        learning_rate=random.uniform(0.0001, 1.0),
        gamma=random.randint(0, 20),
        subsample=random.uniform(0.00001, 1.0),
    )
    param_options.append(params)

print("distributing tests")
# For purely local `multiprocessing`, replace the `discomp` line with the following.
# with multiprocessing.Pool() as pool:
with discomp.Pool() as pool:
    # `discomp.Pool().map` will send the `test_fit` to multiple machines to run in parallel.
    # The amount of machines depends on the number of items in the `param_options` list.
    results = pool.map(test_fit, param_options)

    # For a serial example, replace the above two lines with the following.
    # results = list(map(test_fit, param_options))
    best_index = np.argmax(results)
    print(f"Ran {param_test_count} tests")
    print(f"Best result {results[best_index]:0.2f}")
    print(f"Best params: {param_options[best_index]}")
