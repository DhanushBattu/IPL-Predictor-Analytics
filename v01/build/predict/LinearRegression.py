from converter import *
import pandas as pd
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from scipy import stats


def linear_regression(team1, team2):
    Cleaned_Data_Mod_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Cleaned_Data_Mod.csv")
    df = pd.read_csv(Cleaned_Data_Mod_PATH, converters = {"Team_1":team_converter,
    "Team_2":team_converter, "Toss_Winner":team_converter,"Toss_Decision":toss_dec_converter,
    "Winner_of_Match":team_converter, "City_Played":city_converter})

    

    team1 = team_converter(team1)
    team2 = team_converter(team2)
    df_temp = df[(df.Team_1 == team1) & (df.Team_2 == team2)]

    X = df_temp[['Team_1', 'Team_2', 'City_Played', 'Toss_Winner', 'Toss_Decision']]
    y = df_temp['Winner_of_Match'].values.reshape(-1,1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3)    
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred = lr.predict(X_test)
    res = stats.mode(y_pred)
    res = int(res[0])
    if(abs(team1 - res) >= abs(team2-res)): return res
    else: return team1

