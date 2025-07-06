from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, BaggingClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier
from enum import Enum
from typing import Union

#from django.db import models

ModelType = Union[
    DecisionTreeClassifier,
    LogisticRegression,
    GaussianNB,
    KNeighborsClassifier,
    RandomForestClassifier,
    BaggingClassifier,
    ExtraTreesClassifier,
    GradientBoostingClassifier,
    MLPClassifier
]

class AvailableModels:
    class BlackboxModels(Enum):
        DECISION_TREE = DecisionTreeClassifier()
        LOGISTIC_REGRESSION = LogisticRegression()
        NAIVE_BAYES = GaussianNB()
        KNN = KNeighborsClassifier()
    class WhiteBoxModels(Enum):
        RANDOM_FOREST = RandomForestClassifier()
        BAGGING = BaggingClassifier()
        EXTRA_TREES = ExtraTreesClassifier()
        GRADIENT_BOOSTING = GradientBoostingClassifier()
        MLP = MLPClassifier()
