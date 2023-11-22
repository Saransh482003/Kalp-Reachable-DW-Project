from app import app
from flask import render_template, request, redirect, jsonify
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import requests

sns.set()
sns.set_style("whitegrid")

data = pd.read_csv("app/Mobile Towers Analysis.csv")
coddist = lambda x1, y1, x2, y2: ((x2 - x1)**2 + (y2 - y1)**2)**0.5

@app.route("/")
def home():
    ip_response = requests.get('https://api64.ipify.org?format=json').json()
    ip_address = ip_response["ip"]
    ipapi_response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": ipapi_response.get("city"),
        "region": ipapi_response.get("region"),
        "country": ipapi_response.get("country_name"),
        "latitude": ipapi_response.get("latitude"),
        "longitude": ipapi_response.get("longitude"),
    }
    return render_template("home.html",findme=location_data)

@app.route("/former", methods=["POST"])
def former():
    form = request.form
    conn = form["connector"]
    state = form["state"]
    long = float(form["long"])
    lat = float(form["lat"])
    reff = data[(data["circle"]==state) & (data["radio"]==conn)]
    reff.reset_index(drop=True,inplace=True)
    dister = (((reff["long"]-long)**2+(reff["lat"]-lat)**2)**0.5).sort_values()
    recom = reff.iloc[list(dister.index)]["operator"].head(100).value_counts().index[0]
    ret = reff.iloc[list(dister.index)].head(100)
    recommed = {
        "name": recom,
        "radio":conn,
        "state":state
    }
    plt.figure(figsize=(20,12))
    sns.scatterplot(x=ret["lat"], y=ret["long"], hue=ret["operator"], palette="magma", edgecolor='None', s=100, alpha=0.8)
    sns.scatterplot(x=[lat],y=[long],s=500,color="g",marker="X")
    plt.tick_params(colors="white")
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig("app/static/images/plot.png")
    # plt.show()
    ip_response = requests.get('https://api64.ipify.org?format=json').json()
    ip_address = ip_response["ip"]
    ipapi_response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": ipapi_response.get("city"),
        "region": ipapi_response.get("region"),
        "country": ipapi_response.get("country_name"),
        "latitude": ipapi_response.get("latitude"),
        "longitude": ipapi_response.get("longitude"),
    }
    return render_template("home.html",recommed=recommed,findme=location_data)


if __name__=="__main__":
    app.run(debug=True)