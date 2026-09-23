import os
import subprocess
import sys
from connect import *
from converter import *
from LinearRegression import *
from LogisticRegression import *
from DecisionTreeClassifier import *
from GaussianNaiveBayes import *
from KNeighborsClassifier import *
from RandomForest import *


team1, team2, city, tosswin, algo = user_val()

algo = algo_converter(algo)


def logWinner(m):
    with open("temp.txt", "w") as file:
        file.write(f"{m}")

def main():
    if(algo == 1):
        # execfile('LinearRegression.py')
        # os.system("python LinearRegression.py")
        team_pred = linear_regression(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
    if(algo == 2):
        team_pred = logistic_regression(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
    if(algo == 3):
        team_pred = dec_tree_classifier(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
    if(algo == 4):
        team_pred = gaussian_naive_bayes(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
    if(algo == 5):
        team_pred = knn_classifier(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
    if(algo == 6):
        team_pred = random_forest(team1, team2)
        team_pred = team_converter_back(team_pred)
        # print(team_pred)
        logWinner(team_pred)
