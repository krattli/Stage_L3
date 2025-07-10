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

class AvailableModels(Enum):
    DECISION_TREE = "DECISION_TREE"
    LOGISTIC_REGRESSION = "LOGISTIC_REGRESSION"
    NAIVE_BAYES = "NAIVE_BAYES"
    KNN = "KNN"
    RANDOM_FOREST = "RANDOM_FOREST"
    BAGGING = "BAGGING"
    EXTRA_TREES = "EXTRA_TREES"
    GRADIENT_BOOSTING = "GRADIENT_BOOSTING"
    MLP = "MLP"

MODEL_MAP = {
    AvailableModels.DECISION_TREE: DecisionTreeClassifier(),
    AvailableModels.LOGISTIC_REGRESSION: LogisticRegression(),
    AvailableModels.NAIVE_BAYES: GaussianNB(),
    AvailableModels.KNN: KNeighborsClassifier(),
    AvailableModels.RANDOM_FOREST: RandomForestClassifier(),
    AvailableModels.BAGGING: BaggingClassifier(),
    AvailableModels.EXTRA_TREES: ExtraTreesClassifier(),
    AvailableModels.GRADIENT_BOOSTING: GradientBoostingClassifier(),
    AvailableModels.MLP: MLPClassifier(),
}
