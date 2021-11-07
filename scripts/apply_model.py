import pandas as pd

print("::::MODELING::::")

processed = pd.read_csv("dev/processed.csv")

# Removing labels and creating another dataset for them
all_inputs = processed.iloc[:, :-1].values
all_labels = processed.iloc[:, -1].values

from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV, cross_val_score
#dt_classifier = DecisionTreeClassifier(random_state=0)
#dt_grid_search = GridSearchCV(dt_classifier, scoring="roc_auc", cv=10, param_grid={})
#dt_grid_search.fit(all_inputs, all_labels)
#print('Best score: {}'.format(dt_grid_search.best_score_))

# ...