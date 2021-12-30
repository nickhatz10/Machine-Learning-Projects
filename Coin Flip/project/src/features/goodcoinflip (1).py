# -*- coding: utf-8 -*-
"""GoodCoinFlip.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-qqKPmHfqifQqFB8rvWK5EGyJJqF_sKj
"""

# mount google drive to this notebook to be able to access files in my drive

from google.colab import drive
drive.mount('/content/drive')

# import statements that I will be using for data manipulation
import pandas as pd
import numpy as np

# create links to the csv files for the training and testing data
train_csv = '/content/drive/My Drive/Stat_380/Project2/train.csv'
test_csv = '/content/drive/My Drive/Stat_380/Project2/test.csv'

# use pandas to read the csv files and convert them to pandas dataframes
# give them corresponding variable names

train_data = pd.read_csv(train_csv)
test_data = pd.read_csv(test_csv)

# drop the "Id" column in the train data since we won't be using this
train_data = train_data.drop("id", 1)

# drops the Id column from the test data since we will not be using this
test_data = test_data.drop("id", 1)

# assigns the result column as the variable train_labels
train_labels = train_data['result']

# after assigning this column we will drop the column since we no longer need this column
train_data = train_data.drop('result', 1)

# uses train_test_split to split the training data into a train and test set
# this allows us to see how accurate our predictions were
# it also allows us to fine tune the models hyperparameters so that we can produce a model with the highest accuracy
# we will compare the train and test auc scores to tune these hyperparameters

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_data, train_labels, test_size=0.3, random_state=42)

# import statements for hyperparameter tuning 
# roc-auc curve is important when determining how well a model performs

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# uses the auc-roc curve for hyperparameter tuning of the model
# this tunes the learning rate parameter of the gradient boosting algorithm to prevent overfitting
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

learning_rates = [1, 0.5, 0.25, 0.1, 0.05, 0.01]
train_results = []
test_results = []
for eta in learning_rates:
   model = GradientBoostingClassifier(learning_rate=eta)
   model.fit(X_train, y_train)
   train_pred = model.predict(X_train)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   train_results.append(roc_auc)
   y_pred = model.predict(X_test)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   test_results.append(roc_auc)
from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(learning_rates, train_results, 'b', label='Train AUC')
line2, = plt.plot(learning_rates, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('learning rate')
plt.show()

# uses the auc-roc curve for hyperparameter tuning of the model
# this tunes the n_estimators parameter of the gradient boosting algorithm to prevent overfitting

n_estimators = [1, 2, 4, 8, 16, 32, 64, 100, 200]
train_results = []
test_results = []
for estimator in n_estimators:
   model = GradientBoostingClassifier(n_estimators=estimator)
   model.fit(X_train, y_train)
   train_pred = model.predict(X_train)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   train_results.append(roc_auc)
   y_pred = model.predict(X_test)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   test_results.append(roc_auc)
from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(n_estimators, train_results, 'b', label='Train AUC')
line2, = plt.plot(n_estimators, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('n_estimators')
plt.show()

# uses the auc-roc curve for hyperparameter tuning of the model
# this tunes the max depth parameter of the gradient boosting algorithm to prevent overfitting

max_depths = np.linspace(1, 32, 10, endpoint=True)
train_results = []
test_results = []
for max_depth in max_depths:
   model = GradientBoostingClassifier(max_depth=max_depth)
   model.fit(X_train, y_train)
   train_pred = model.predict(X_train)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_train, train_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   train_results.append(roc_auc)
   y_pred = model.predict(X_test)
   false_positive_rate, true_positive_rate, thresholds = roc_curve(y_test, y_pred)
   roc_auc = auc(false_positive_rate, true_positive_rate)
   test_results.append(roc_auc)
from matplotlib.legend_handler import HandlerLine2D
line1, = plt.plot(max_depths, train_results, 'b', label='Train AUC')
line2, = plt.plot(max_depths, test_results, 'r', label='Test AUC')
plt.legend(handler_map={line1: HandlerLine2D(numpoints=2)})
plt.ylabel('AUC score')
plt.xlabel('Tree depth')
plt.show()

# using gradient boosting to make a prediction for this assignment
from sklearn.ensemble import GradientBoostingClassifier

# uses specific hyperparameters chosen based on the roc-auc curves above
gbc = GradientBoostingClassifier(learning_rate=0.1, n_estimators = 100, max_depth = 5)

# fits the gradient boosting classifier for prediction on the train data
gbc.fit(train_data, train_labels)

# predict_proba gives the percentage probability for the binary 0 and 1 outcome
# I only want to know the percentage probability for the 1 prediction which is what the [:, 1] does
prob_preds = gbc.predict_proba(test_data)[:, 1]

# imports the sample submission csv file
sample_csv = '/content/drive/My Drive/Stat_380/Project2/samp_sub.csv'



# uses pandas to read this sample submission and then convert it to a dataframe
sample_sub = pd.read_csv(sample_csv)

# replaces the predictions on the sample submission dataframe with the predictions that we made
sample_sub['result'] = prob_preds

# then saves this new dataframe with our predictions in it to a csv file so that we can submit to kaggle

sample_sub.to_csv('/content/drive/My Drive/Stat_380/Project2/submission3.csv', index = False, header=True)