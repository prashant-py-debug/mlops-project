import pandas as pd
from sklearn.model_selection import train_test_split


def test_load_data():
    """
    loads data from csv file
    """

    data = pd.read_csv("banana/banana.csv", names=["At1", "At2", "Class"])
    X = data.drop(columns="Class")
    _ = data.Class
    expectation = (2, 1)
    actual = (X.shape[1], 1)
    print(actual)
    assert expectation == actual


def test_prepare():
    """
    splits data into train and test set
    """
    data = pd.read_csv("banana/banana.csv", names=["At1", "At2", "Class"])
    X = data.drop(columns="Class")
    y = data.Class

    X_train, X_test, _, _ = train_test_split(X, y, test_size=0.2, random_state=1234)
    actual = (X_train.shape[1], X_test.shape[1], 1, 1)
    expectation = (2, 2, 1, 1)
    assert expectation == actual
