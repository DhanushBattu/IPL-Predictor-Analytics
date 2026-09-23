from connect import *

def team_converter(s):
    s = s.lower()
    if(s == "csk"): return 1
    if(s == "mi"): return 2
    if(s == "srh"): return 3
    if(s == "kkr"): return 4
    if(s == "dc"): return 5
    if(s == "dec_c"): return 6
    if(s == "pbks"): return 7
    if(s == "rcb"): return 8
    if(s == "gl"): return 9
    if(s == "pw"): return 10
    if(s == "rps"): return 11
    if(s == "rr"): return 12
    if(s == "ktk"): return 13
    return -1

def toss_win(s):
    s = s.lower()
    if(s == "team1"): return 1
    if(s == "team2"): return 2
    return -1

def city_converter(s):
    s = s.lower()
    if(s == 'abu dhabi'): return 1
    if(s == 'ahmedabad'): return 2
    if(s == 'bangalore' or s == 'bengaluru'): return 3
    if(s == 'bloemfontein'): return 4
    if(s == 'cape town'): return 5
    if(s == 'centurion'): return 6
    if(s == 'chandigarh'): return 7
    if(s == 'chennai'): return 8
    if(s == 'cuttack'): return 9
    if(s == 'delhi'): return 10
    if(s == 'dharamsala'): return 11
    if(s == 'dubai'): return 12
    if(s == 'east london'): return 13
    if(s == 'hyderabad'): return 14
    if(s == 'indore'): return 15
    if(s == 'jaipur'): return 16
    if(s == 'johannesburg'): return 17
    if(s == 'kanpur'): return 18
    if(s == 'kimberley'): return 19
    if(s == 'kochi'): return 20
    if(s == 'kolkata'): return 21
    if(s == 'mumbai'): return 22
    if(s == 'na'): return 23
    if(s == 'nagpur'): return 24
    if(s == 'port elizabeth'): return 25
    if(s == 'pune'): return 26
    if(s == 'raipur'): return 27
    if(s == 'rajkot'): return 28
    if(s == 'ranchi'): return 29
    if(s == 'sharjah'): return 30
    if(s == 'visakhapatnam'): return 31
    return -1

def team_converter_back(m):
    if(m == 1): return "CSK"
    if(m == 2): return "MI"
    if(m == 3): return "SRH"
    if(m == 4): return "KKR"
    if(m == 5): return "DC"
    if(m == 6): return "DEC_C"
    if(m == 7): return "PBKS"
    if(m == 8): return "RCB"
    if(m == 9): return "GL"
    if(m == 10): return "PW"
    if(m == 11): return "RPS"
    if(m == 12): return "RR"
    if(m == 13): return "KTK"
    return -1

def algo_converter(s):
    s = s.lower()
    if(s == "linearregression"): return 1
    if(s == "logisticregression"): return 2
    if(s == "decisiontreeclassifier"): return 3
    if(s == "gaussiannaivebayes"): return 4
    if(s == "knnclassifier"): return 5
    if(s == "randomforest"): return 6
    return -1

def toss_dec_converter(s):
    s = s.lower()
    if(s == "field"): return 1
    if(s == "bat"): return 2
    return -1



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