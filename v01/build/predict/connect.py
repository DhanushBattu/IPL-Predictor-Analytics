import pymysql

def user_val():

    conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "", database = "ipldb")

    cursor = conn.cursor()

    selectquery = "select * from iplinfodb limit 1"
    cursor.execute(selectquery)
    records = cursor.fetchall()

    for row in records:
        # print("Team1:",row[0]); 
        t1 = row[0]
        # print("Team2:",row[1]); 
        t2 = row[1]
        # print("City:",row[2]); 
        t3 = row[2]
        # print("Toss:",row[3]); 
        t4 = row[3]
        # print("Toss:",row[4]); 
        t5 = row[4]

    cursor.close()

    conn.close()

    return t1,t2,t3,t4,t5

