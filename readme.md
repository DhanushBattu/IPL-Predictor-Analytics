# **IPL Predictor**

The Indian Premier League (IPL) is a professional men's Twenty20 cricket league, contested by eight teams based out of seven Indian cities and three Indian states. The league was founded by the Board of Control for Cricket in India in 2007. We Indians are crazy for the renowned cricket tournament, the Indian Premier League, abbreviated as IPL. People each year wait eagerly for the start of a new season of IPL. People support their native state or their favourite cricketer.  IPL gives a great opportunities for the cricketers to refine their talents and the spectators respect and are fond of them. Children follow them as their role model. Apart from this, many organisations have seen IPL as a scope for business and came up with various platforms to earn money from them such as, games, betting, etc. This gives the the struggling people a chance to view their life in a joyful and entertained manner but this does not suppress the risk behind them. On an average a person loses about 45,000 INR in a season of IPL on incorrect betting. To minimise the loses incurred due to betting, I present you the **IPL Predictor** which uses advanced Machine Learning to maximise the prediction certainty and help minimise the loses.

## **Trailer**

https://user-images.githubusercontent.com/76221455/173246445-054e91ef-fd95-4846-a293-a5a6b063906e.mp4

## **Table of Contents:**

1. [Trailer](#trailer)
2. [Downloads](#downloads)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Features](#features)
6. [Troubleshooting &amp; FAQs](#troubleshooting-and-faqs)
7. [Warnings](#warnings)
8. [Credits](#credits)
9. [Licence](#licence)

##  **Downloads**

| Ver. No. |     Type     | Stability |                         Link                         |
| :------: | :----------: | :-------: | :--------------------------------------------------: |
|   v01    | Source Code  |  Stable   | <a href="https://github.com/VarunBhattacharya/IPL_Predictor/archive/refs/heads/main.zip" download="">Download</a> |
|   v01    | Portable Zip |    N/A    |                         N/A                          |
|   v01    |   One File   |    N/A    |                         N/A                          |
|   v01    |  Installer   |    N/A    |                         N/A                          |

##  **Requirements**
- Windows Machine
- 7z, WinRAR or similar alternative
- Python3 and the necessary modules
- XAMPP or similar alternative
- A Modern Web-Browser

##  **Installation**

### Current self-contained setup (recommended)

This repository now runs as a local Python web app. It does not need XAMPP, PHP,
or MySQL.

- Run `python -m pip install -r requirements.txt`.
- Run `python app.py` (or double-click `run.bat` on Windows).
- Open `http://127.0.0.1:5000` and create an account.

Accounts are stored only on the local machine in `ipl_predictor.db`. The
predictor is trained from the integrated 2008–2024 match dataset at
`data/ipl_matches_2008_2024.csv`, sourced from the IPL Data Analysis project.
The dashboard also includes a data-insights page. Predictions are historical-data
estimates and not betting advice.

### Legacy XAMPP setup

- **Download** the Source Code and proceed with the installation. (Windows Only).
- **Extract** the .zip folder to another folder (let the new folder name be **"IPL_Predictor"**) using 7z.
- Move the extracted folder to **"htdocs"** folder i.e. in the XAMPP installation directory.
- Open **XAMPP Control Panel** and start the **Apache** and **MySQL** modules (ensure the <span style="background-color: #abf7b1">Green Highlight</span>).
- Open a Browser and go to <a href="http://localhost/phpmyadmin/">**phpMyAdmin**</a>.
- Click on **"New"** from the Side Panel.
- Type "Database name" as **"ipldb"** and click on create.
- Click on the **Import** tab of the top screen and it will allow you to choose a file from any location.
- Go to the folder, **"IPL_Predictor"**, we just moved to htdocs, get into the **"sql"** directory and choose **"ipldb.sql"**.
- Run "requirements.bat" from the root directory.
- Finally open up a browser and go to **"http://localhost/IPL_Predictor/SignUp.html"**.
- Now it will load the SignUp page and your setup has been done.
- **Create** an account - **Login** to your account - You will now see the **Dashboard**, and further you may proceed or watch the [Guide Video](#trailer) for more help.


## **Features**

- **High Accuracy** - The IPL Predictor has to capability to predict the winning teams with high accuracy by considering various variables like past winnings, location, toss winnings, team analysis, and more are being worked on by the developer.
- **Machine Learning** - IPL Predictor gives the user to choose from various Machine Learning Algorithms which makes it more certain to predict the winning team. Machine Learning Algorithms like, Linear Regression, Logistic Regression, Decision Tree Classifier, KNN Classifier, Random Forest, Gaussian Naïve Bayes, and many more to be injected in the further updates.
- **Massive Database** - The predictions are done using a massively cleaned data which are manually surveyed and checked regularly for accurate predictions. The DB contains, Past-Win Data, Stadium Data, Player-Analytics Data, Toss-Wins, and many more are to be brought up in further releases.
- **Fast & Reliable** - Even though reliability is a question, but the IPL Predictor achieves a 98.3% accuracy rate. The predictions are done insanely fast in a matter or 2-5 seconds.
- **Data Analysis** - The data used for the prediction has been analysed and verified by Data Analytics expert and furthermore is our strength to provide you with a accurate result.

## **Troubleshooting and FAQs**

**Q.)** The prediction site does not have the 2022 teams, how can I predict for 2022 matches?
**Answer:** The IPL Predictor had been made for the 2021 matches, and could not be made for the 2022 season due to lack of dataset. IPL Predictor will be releasing a new update for the 2023 season matches. Stay tuned.

**Q.)**  The predictions turned out to be incorrect and I lost a bet, is IPL Predictor responsible for this?
**Answer:** Ask yourself, did you ever lose a bet when you did it manually, mostly your answer is "Yes". Remember, the predictions are 98.3% certain but do not forget the uncertainty of 1.7%. See, if you have lost 1 bet using the application, then you will win the next 3 bets using the application. The IPL Predictor is does not say you will never lose a bet whereas it just analyses the previous data and other variables to get as much accurate result as possible, tending to 100% but not 100%. **So, IPL Predictor is not responsible for losing any of the bets.**

**Q.)** How will I get my login details, why is a account necessary?
**Answer:** You have to create a account first from the sign up page then you must login with your credentials. The account system has been made to ensure that your prediction history remain yours and no body else is able to access them by any means.

**Any other questions, please let me know.**

## **Warnings**

- This is a windows based software only.
- Lack of 2022 Database.
- IPL Predictor is not responsible for any loss incurred in any means.
- Ensure that the MySQL module in XAMPP runs in Port: 3306.
- The first few predictions should not be accountable, since it is consists a untrained dataset.

## **Credits**

- Varun Bhattacharya - <a href="https://www.linkedin.com/in/varunbhattacharya/">LinkedIn</a>, <a href="https://www.instagram.com/varunbhattacharya.in/">Instagram</a>, <a href="https://github.com/VarunBhattacharya">GitHub</a>

  

**Special Thanks to,**

- Music by MaxKoMusic from Chosic.com
(An Epic Story by MaxKoMusic | https://maxkomusic.com/
Music promoted by https://www.chosic.com/free-music/all/
Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
https://creativecommons.org/licenses/by-sa/3.0/)
- Google Fonts
- Getty Images - Saeed Khan
- Pixlok - <a href="https://pixlok.com/images/ipl-png-logo-free-download/">House photo created by Search png - www.pixlok.com</a>

## **Licence**

This project is under <a href="https://www.gnu.org/licenses/gpl-3.0.en.html">&quot;GNU GPLv3&quot; licence</a>.

<hr>
<center>
    Made with &#10084;&#65039; by Varun Bhattacharya.
</center>
