"""Self-contained local web app for the IPL Predictor dataset.

Run with ``python app.py`` and open http://127.0.0.1:5000.
Accounts are stored locally in ``ipl_predictor.db``; no PHP, XAMPP, or MySQL
installation is required.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

import pandas as pd
from flask import Flask, flash, redirect, render_template_string, request, session, url_for
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.base import BaseEstimator, TransformerMixin
from werkzeug.security import check_password_hash, generate_password_hash


ROOT = Path(__file__).resolve().parent
BUILD_DIR = ROOT / "v01" / "build"
DATA_FILE = ROOT / "data" / "ipl_matches_2008_2024.csv"
DATABASE = ROOT / "ipl_predictor.db"

app = Flask(__name__, static_folder=str(BUILD_DIR), static_url_path="/static")
app.config["SECRET_KEY"] = "change-this-local-development-secret"

TEAMS = {
    "CSK": "Chennai Super Kings",
    "DC": "Delhi Capitals",
    "RCB": "Royal Challengers Bangalore",
    "KKR": "Kolkata Knight Riders",
    "MI": "Mumbai Indians",
    "SRH": "Sunrisers Hyderabad",
    "RR": "Rajasthan Royals",
    "PBKS": "Punjab Kings",
    "GT": "Gujarat Titans",
    "LSG": "Lucknow Super Giants",
}
TEAM_NAMES = {
    **TEAMS,
    "Dec_C": "Deccan Chargers",
    "GL": "Gujarat Lions",
    "KXIP": "Kings XI Punjab",
    "KTK": "Kochi Tuskers Kerala",
    "PW": "Pune Warriors",
    "RPS": "Rising Pune Supergiant",
}
TEAM_ALIASES = {
    "Chennai Super Kings": "CSK",
    "Delhi Capitals": "DC",
    "Delhi Daredevils": "DC",
    "Royal Challengers Bangalore": "RCB",
    "Royal Challengers Bengaluru": "RCB",
    "Kolkata Knight Riders": "KKR",
    "Mumbai Indians": "MI",
    "Sunrisers Hyderabad": "SRH",
    "Rajasthan Royals": "RR",
    "Punjab Kings": "PBKS",
    "Kings XI Punjab": "PBKS",
    "Gujarat Titans": "GT",
    "Lucknow Super Giants": "LSG",
    "Deccan Chargers": "Dec_C",
    "Gujarat Lions": "GL",
    "Kochi Tuskers Kerala": "KTK",
    "Pune Warriors": "PW",
    "Rising Pune Supergiant": "RPS",
    "Rising Pune Supergiants": "RPS",
}
CITIES = [
    "Abu Dhabi", "Ahmedabad", "Bangalore", "Bengaluru", "Bloemfontein", "Cape Town",
    "Centurion", "Chandigarh", "Chennai", "Cuttack", "Delhi", "Dharamsala", "Dubai",
    "Durban", "East London", "Hyderabad", "Indore", "Jaipur", "Johannesburg", "Kanpur",
    "Kimberley", "Kochi", "Kolkata", "Mumbai", "Nagpur", "Port Elizabeth", "Pune",
    "Guwahati", "Lucknow", "Mohali", "Navi Mumbai", "Raipur", "Rajkot", "Ranchi", "Sharjah", "Visakhapatnam",
]
ALGORITHMS = {
    "linear": "Linear Regression",
    "logistic": "Logistic Regression",
    "tree": "Decision Tree Classifier",
    "naive_bayes": "Gaussian Naive Bayes",
    "knn": "KNN Classifier",
    "forest": "Random Forest",
}
FEATURES = ["Team_1", "Team_2", "City_Played", "Toss_Winner", "Toss_Decision"]


def db() -> sqlite3.Connection:
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def initialise_database() -> None:
    with db() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                gender TEXT NOT NULL,
                phone TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )"""
        )


def load_match_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Load the 2008–2024 analysis data and make team labels model-friendly."""
    raw = pd.read_csv(DATA_FILE)
    data = raw.rename(columns={
        "team1": "Team_1", "team2": "Team_2", "city": "City_Played",
        "toss_winner": "Toss_Winner", "toss_decision": "Toss_Decision",
        "winner": "Winner_of_Match",
    }).copy()
    for column in ("Team_1", "Team_2", "Toss_Winner", "Winner_of_Match"):
        data[column] = data[column].map(TEAM_ALIASES)
    data = data.dropna(subset=FEATURES + ["Winner_of_Match"])
    return raw, data


def build_models(data: pd.DataFrame) -> tuple[dict[str, Any], LabelEncoder]:
    """Train all selectable models once from the 1,095-match historical dataset."""

    labels = LabelEncoder()
    target = labels.fit_transform(data["Winner_of_Match"])
    def transformer() -> ColumnTransformer:
        return ColumnTransformer(
            [("categories", OneHotEncoder(handle_unknown="ignore"), FEATURES)],
            remainder="drop",
        )
    models: dict[str, Any] = {
        "linear": Pipeline([( "features", transformer()), ("model", LinearRegression())]),
        "logistic": Pipeline([( "features", transformer()), ("model", LogisticRegression(max_iter=2000))]),
        "tree": Pipeline([( "features", transformer()), ("model", DecisionTreeClassifier(random_state=42))]),
        # GaussianNB needs a dense matrix after the categorical encoding.
        "naive_bayes": Pipeline([( "features", transformer()), ("dense", _Dense()), ("model", GaussianNB())]),
        "knn": Pipeline([( "features", transformer()), ("model", KNeighborsClassifier(n_neighbors=9))]),
        "forest": Pipeline([( "features", transformer()), ("model", RandomForestClassifier(n_estimators=250, random_state=42))]),
    }
    for model in models.values():
        model.fit(data[FEATURES], target)
    return models, labels


class _Dense(BaseEstimator, TransformerMixin):
    """Small sklearn-compatible transformer for GaussianNB's dense input."""

    def fit(self, _x: Any, _y: Any = None) -> "_Dense":
        return self

    def transform(self, values: Any) -> Any:
        return values.toarray() if hasattr(values, "toarray") else values


initialise_database()
RAW_MATCHES, TRAINING_DATA = load_match_data()
MODELS, LABELS = build_models(TRAINING_DATA)


def predict(form: dict[str, str]) -> str:
    row = pd.DataFrame([{
        "Team_1": form["team1"],
        "Team_2": form["team2"],
        "City_Played": form["city"],
        "Toss_Winner": form["team1"] if form["tosswin"] == "team1" else form["team2"],
        "Toss_Decision": form["tossdecision"],
    }])
    raw_prediction = MODELS[form["algorithm"]].predict(row)[0]
    if form["algorithm"] == "linear":
        raw_prediction = int(round(float(raw_prediction)))
        raw_prediction = max(0, min(raw_prediction, len(LABELS.classes_) - 1))
    return str(LABELS.inverse_transform([int(raw_prediction)])[0])


BASE = """
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>IPL Predictor</title><link rel="stylesheet" href="{{ url_for('static', filename='Selection.css') }}">
<style>body{min-height:100vh;margin:0}.content{position:relative;top:auto;left:auto;transform:none;width:min(680px,calc(100% - 48px));margin:60px auto 80px;box-sizing:border-box}input,select{box-sizing:border-box;padding:8px;margin:4px;max-width:100%}label{display:block;margin:12px 0 3px}.message{padding:10px;border-radius:8px;background:#651c1c;margin:10px 0}.subtle{color:#e4e4e4;font-size:.9rem}.row{display:grid;grid-template-columns:1fr 1fr;gap:12px}.footer{height:auto;min-height:28px;padding:5px 0}</style>
</head><body><main class="content"><h1><img src="{{ url_for('static', filename='assets/Batter_Logo.png') }}" id="bat_logo" alt="IPL Predictor logo"> IPL Predictor</h1>
{% with messages = get_flashed_messages() %}{% for message in messages %}<p class="message">{{ message }}</p>{% endfor %}{% endwith %}
{{ body|safe }}</main><footer class="footer"><div style="text-align:center">Local IPL Predictor &middot; historical data through 2021</div></footer></body></html>
"""


def page(body: str, **context: Any) -> str:
    return render_template_string(BASE, body=render_template_string(body, **context))


@app.get("/")
def home() -> str:
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup() -> str:
    if request.method == "POST":
        fields = {name: request.form.get(name, "").strip() for name in ("name", "email", "gender", "phone", "username", "password")}
        if not all(fields.values()):
            flash("Please complete every field.")
        elif len(fields["username"]) > 30:
            flash("Username must be 30 characters or fewer.")
        else:
            try:
                with db() as connection:
                    connection.execute("INSERT INTO users(name,email,gender,phone,username,password_hash) VALUES(?,?,?,?,?,?)", (fields["name"], fields["email"], fields["gender"], fields["phone"], fields["username"], generate_password_hash(fields["password"])))
                flash("Account created. Please log in.")
                return redirect(url_for("login"))
            except sqlite3.IntegrityError:
                flash("That email address or username is already registered.")
    return page("""
        <h2>Sign up</h2><form method="post"><label>Name <input name="name" required></label><label>Email <input type="email" name="email" required></label>
        <label>Gender <select name="gender" required><option value="">Select</option><option>M</option><option>F</option><option>Prefer not to say</option></select></label>
        <label>Phone number <input name="phone" inputmode="tel" required></label><label>Username <input name="username" required></label><label>Password <input type="password" name="password" required></label>
        <p><button id="submit">Create account</button></p></form><p class="subtle">Already registered? <a href="{{ url_for('login') }}">Log in</a>.</p>""")


@app.route("/login", methods=["GET", "POST"])
def login() -> str:
    if request.method == "POST":
        with db() as connection:
            user = connection.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username", "").strip(),)).fetchone()
        if user and check_password_hash(user["password_hash"], request.form.get("password", "")):
            session["user_id"] = user["id"]
            session["name"] = user["name"]
            return redirect(url_for("dashboard"))
        flash("Incorrect username or password.")
    return page("""<h2>Log in</h2><form method="post"><label>Username <input name="username" required autofocus></label><label>Password <input type="password" name="password" required></label><p><button id="submit">Log in</button></p></form><p class="subtle">New here? <a href="{{ url_for('signup') }}">Create an account</a>.</p>""")


def require_login() -> Any:
    if not session.get("user_id"):
        flash("Please log in to make a prediction.")
        return redirect(url_for("login"))
    return None


@app.get("/dashboard")
def dashboard() -> str:
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    return page("""<h2>Welcome, {{ name }}</h2><p>Use the included IPL match history (2008–2024) to compare two teams with one of six models.</p><p><a href="{{ url_for('selection') }}"><button id="myBtn2">Start prediction</button></a> <a href="{{ url_for('analytics') }}">Explore data insights</a> &middot; <a href="{{ url_for('logout') }}">Log out</a></p><p class="subtle">Predictions are historical-data estimates, not betting advice.</p>""", name=session["name"])


@app.route("/predict", methods=["GET", "POST"])
def selection() -> str:
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    if request.method == "POST":
        form = {key: request.form.get(key, "") for key in ("team1", "team2", "city", "tosswin", "tossdecision", "algorithm")}
        if not all(form.values()):
            flash("Select a value for every prediction field.")
        elif form["team1"] == form["team2"]:
            flash("Choose two different teams.")
        else:
            winner = predict(form)
            return page("""<h2>Prediction result</h2><p>The <strong>{{ algorithm }}</strong> model predicts:</p><h2>{{ winner_name }}</h2><p class="subtle">{{ team1_name }} vs {{ team2_name }} in {{ city }}; toss won by {{ toss_name }}, who chose to {{ toss_decision }}.</p><p><a href="{{ url_for('selection') }}"><button id="myBtn2">Make another prediction</button></a></p>""", algorithm=ALGORITHMS[form["algorithm"]], winner_name=TEAM_NAMES.get(winner, winner), team1_name=TEAMS[form["team1"]], team2_name=TEAMS[form["team2"]], city=form["city"], toss_name=TEAMS[form["team1"] if form["tosswin"] == "team1" else form["team2"]], toss_decision=form["tossdecision"])
    return page("""<h2>Match details</h2><form method="post"><div class="row"><label>Team 1<select name="team1" required><option value="">Select team</option>{% for code, name in teams.items() %}<option value="{{ code }}">{{ name }}</option>{% endfor %}</select></label><label>Team 2<select name="team2" required><option value="">Select team</option>{% for code, name in teams.items() %}<option value="{{ code }}">{{ name }}</option>{% endfor %}</select></label></div><label>City<select name="city" required><option value="">Select city</option>{% for city in cities %}<option>{{ city }}</option>{% endfor %}</select></label><label>Toss winner</label><label><input type="radio" name="tosswin" value="team1" required> Team 1</label><label><input type="radio" name="tosswin" value="team2" required> Team 2</label><label>Toss decision <select name="tossdecision" required><option value="">Select decision</option><option value="bat">Bat</option><option value="field">Field</option></select></label><label>Model<select name="algorithm" required><option value="">Select model</option>{% for code, name in algorithms.items() %}<option value="{{ code }}">{{ name }}</option>{% endfor %}</select></label><p><button id="submit">Predict winner</button></p></form><p><a href="{{ url_for('dashboard') }}">Back to dashboard</a></p>""", teams=TEAMS, cities=CITIES, algorithms=ALGORITHMS)


@app.get("/analytics")
def analytics() -> str:
    redirect_response = require_login()
    if redirect_response:
        return redirect_response
    completed = RAW_MATCHES.dropna(subset=["winner", "toss_winner"])
    toss_win_rate = round((completed["winner"] == completed["toss_winner"]).mean() * 100, 1)
    team_wins = completed["winner"].map(TEAM_ALIASES).value_counts().head(5)
    leaders = [(TEAM_NAMES.get(code, code), int(wins)) for code, wins in team_wins.items()]
    players = RAW_MATCHES["player_of_match"].dropna().value_counts().head(5).items()
    latest = RAW_MATCHES[RAW_MATCHES["season"].astype(str) == "2024"]
    latest_final = latest[latest["match_type"] == "Final"]
    champion = latest_final["winner"].iloc[0] if not latest_final.empty else "Not available"
    return page("""<h2>IPL data insights</h2><p class="subtle">Derived from the integrated 2008–2024 match dataset.</p><div class="row"><p><strong>{{ match_count }}</strong><br>completed matches</p><p><strong>{{ toss_rate }}%</strong><br>toss winners also won</p><p><strong>{{ champion }}</strong><br>2024 champion</p><p><strong>{{ season_count }}</strong><br>seasons represented</p></div><h3>Most match wins</h3><ol>{% for team, wins in leaders %}<li>{{ team }} — {{ wins }} wins</li>{% endfor %}</ol><h3>Most Player of the Match awards</h3><ol>{% for player, awards in players %}<li>{{ player }} — {{ awards }}</li>{% endfor %}</ol><p><a href="{{ url_for('selection') }}"><button id="myBtn2">Use the predictor</button></a> <a href="{{ url_for('dashboard') }}">Back to dashboard</a></p>""", match_count=len(completed), toss_rate=toss_win_rate, champion=champion, season_count=RAW_MATCHES["season"].nunique(), leaders=leaders, players=players)


@app.get("/logout")
def logout() -> Any:
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
