from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import ExtraTreeRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class LinRegLearner:
    """Linear regression learning machine"""

    def __init__():
        self.model = LinearRegression(n_jobs = -1)

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)

class KNNLearner:
    """K-nearest-neighbor regressor"""

    def __init__(k = 3):
        self.model = KNeighborsRegressor(n_neighbors = k, weights = 'distance', algorithm = 'brute')

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)

class DTLearner:
    """Decision tree regressor"""

    def __init__(max_depth = None):
        self.model = DecisionTreeRegressor(max_depth = max_depth)

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)

class ETLearner:
    """Extra tree regressor"""

    def __init__():
        self.model = ExtraTreeRegressor()

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)

class ETELearner:
    """Extra trees ensemble regressor"""

    def __init__(max_depth = None):
        self.model = ExtraTreesRegressor(max_depth = max_depth)

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)

class RFELearner:
    """Random forest ensemble regressor"""

    def __init__():
        self.model = ExtraTreesRegressor()

    def fit(X, y):
        self.model.fit(X, y)

    def predict(X):
        return self.model.predict(X)

    def score(X, y):
        return self.model.score(X, y)
