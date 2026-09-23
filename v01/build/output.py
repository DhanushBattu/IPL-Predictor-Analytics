# !/usr/bin/env python
import cgi
import os
import pymysql
import sys
sys.path.insert(1,"predict")
import predict.main

def getAlgo():
    conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "", database = "ipldb")

    cursor = conn.cursor()

    selectquery = "select Algorithm from iplinfodb limit 1"
    cursor.execute(selectquery)
    records = cursor.fetchall()

    for row in records:
        algo = row[0]

    sql_del_query = """truncate iplinfodb"""
    cursor.execute(sql_del_query)

    cursor.close()

    conn.close()
    return algo

def getWinner():
    predict.main.main()
    with open("temp.txt", "r") as file:
        winner = str(file.read()).strip()
    os.remove("temp.txt")
    return winner
    
def algoPrint(s):
    s = s.lower()
    if(s == "linearregression"): return 'Linear Regression'
    if(s == "logisticregression"): return 'Logistic Regression'
    if(s == "decisiontreeclassifier"): return 'Decision Tree Classifier'
    if(s == "gaussiannaivebayes"): return 'Gaussian Naive Bayes'
    if(s == "knnclassifier"): return 'KNN Classifier'
    if(s == "randomforest"): return 'Random Forest'
    return -1

def teamPrint(s):
    s = s.lower()
    if(s == "csk"): return 'Chennai Super Kings'
    if(s == "mi"): return 'Mumbai Indians'
    if(s == "srh"): return 'Sunrisers Hyderabad'
    if(s == "kkr"): return 'Kolkata Knight Riders'
    if(s == "dc"): return 'Delhi Capitals'
    if(s == "dec_c"): return 'Deccan Chargers'
    if(s == "pbks"): return 'Punjab Kings'
    if(s == "rcb"): return 'Royal Challengers Bangalore'
    if(s == "gl"): return 'Gujarat Lions'
    if(s == "pw"): return 'Pune Warriors'
    if(s == "rps"): return 'Rising Pune Supergiant'
    if(s == "rr"): return 'Rajasthan Royals'
    if(s == "ktk"): return 'Kochi Tuskers Kerala'
    return -1

algorithm = algoPrint(getAlgo())
winner = teamPrint(getWinner())


strhtml = """
<html>
    <head>
        <title>
            IPL Predictor Machine
        </title>
        <link rel="stylesheet" href="style4.css">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <meta name="viewport" content="width=device-width, initial-scale=1" charset="UTF-8">
    </head>

    <body>
        <div class = "content" align = "center">
            <h1><img src = assets\Batter_Logo.png id = "bat_logo" align = "center">&nbsp;
                <font size = "20">IPL Predictor</font>
            </h1>
            <p>
                <br>
                The Winner according to the <br><br>
                <font style="font-size: 35; font-family: Consolas; color: #ffffff; font-weight: bold italic">
                """+ '<font style="font-size: 35; font-family: Consolas; color: #ffffff; font-weight: bold italic">' + algorithm + ' </font>'
                

strhtml2 = """
                </font><br><br>
                algorithm is <br><br>
                <font style="font-size: 35; font-family: Consolas; color: #ffffff; font-weight: bold italic">
                """+ '<font style="font-size: 35; font-family: Consolas; color: #ffffff; font-weight: bold italic">' + winner + ' </font><br><br>'

strhtml3 = """
                </font>
            </p>
        </div>

        <div class = "footer">
            <div style = "text-align: center">
                <span style = " float: left">
                    &nbsp&nbspCrafted with &#10084;&#65039; by Varun Bhattacharya
                </span>
                <span style = "float: right">
                    Follow me on:
                    <a href="https://www.instagram.com/varunbhattacharya.in/">
                        <b style="font-size:17px" class="fa">&#xf16d;</b>
                    </a>
                    <a href="https://github.com/VarunBhattacharya">
                        <b style="font-size:17px" class="fa">&#xf09b;</b>
                    </a>
                    &nbsp;&nbsp;
                </span>
            </div>
        </div>

        <script src="app3.js"></script>

    </body>
</html>
"""

strhtml = strhtml + strhtml2 + strhtml3
print(strhtml)
