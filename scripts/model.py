# imports
import os
import mlflow
import argparse

import pandas as pd
import lightgbm as lgbm
import matplotlib.pyplot as plt

from sklearn.metrics import log_loss, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


# define functions
def main(args):
    mlflow.autolog()

    # setup parameters
    num_boost_round = args.num_boost_round
    params = {
        "objective": "multiclass",
        "num_class": 100,
        "boosting": args.boosting,
        "num_iterations": args.num_iterations,
        "num_leaves": args.num_leaves,
        "num_threads": args.num_threads,
        "learning_rate": args.learning_rate,
        "metric": args.metric,
        "seed": args.seed,
        "verbose": args.verbose,
    }

    df = pd.read_csv(args.data).head(5000)
    X_train, X_test, y_train, y_test, enc = preprocess_data(df)

    model = train(params, num_boost_round, X_train, X_test, y_train, y_test)


def preprocess_data(df):

    #splitting df
    X = df.drop(['Overall'], axis=1)
    X = df[['International Reputation', 'Special']]
    y = df['Overall'] # specify

    # encode y
    enc = LabelEncoder()
    y = enc.fit_transform(y)

    # train/test splitting
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)
    return X_train, X_test, y_train, y_test, enc


# train the light gradient boosting model
def train(params, num_boost_round, X_train, X_test, y_train, y_test):
    train_data = lgbm.Dataset(X_train, label=y_train)
    test_data = lgbm.Dataset(X_test, label=y_test)

    # train model
    model = lgbm.train(
        params,
        train_data,
        num_boost_round=num_boost_round,
        valid_sets=[test_data],
        valid_names=["test"],
    )
    return model

def parse_args():
    parser = argparse.ArgumentParser()

    # add parser arguments
    parser.add_argument("--data", type=str)
    parser.add_argument("--num-boost-round", type=int, default=10)
    parser.add_argument("--boosting", type=str, default="gbdt")
    parser.add_argument("--num-iterations", type=int, default=16)
    parser.add_argument("--num-leaves", type=int, default=31)
    parser.add_argument("--num-threads", type=int, default=0)
    parser.add_argument("--learning-rate", type=float, default=0.1)
    parser.add_argument("--metric", type=str, default="multi_logloss")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--verbose", type=int, default=0)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
