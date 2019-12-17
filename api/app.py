from flask import Flask, jsonify, render_template
from strategy.SmaCross import SmaCross
from backtesting.test import GOOG
from backtesting import Backtest
from bokeh.embed import components
from bokeh.client import pull_session
from bokeh.embed import server_session, json_item
import pandas as pd
import json

app = Flask(__name__)


@app.route("/", methods=["GET"])
def bkapp_page():

    with pull_session(url="http://localhost:5006/sliders") as session:

        # update or customize that session
        session.document.roots[0].children[
            1
        ].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        script = server_session(
            session_id=session.id, url="http://localhost:5006/sliders"
        )

        # use the script in the rendered page
        return render_template("embed.html", script=script, template="Flask")


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'


@app.route("/test")
def test_goog():
    bt = Backtest(GOOG, SmaCross, cash=10000, commission=0.002)
    result = bt.run()[:-1].to_json()
    return result


@app.route("/visual")
def visual():
    bt = Backtest(GOOG, SmaCross, cash=10000, commission=0.002)
    bt.run()
    plot = bt.plot()
    script, div = components(plot)
    return render_template("visual.html", script=script, div=div)


@app.route("/upload")
def upload():
    # TODO: consider a database, ie.sqlite
    data = pd.read_excel(
        "Convertible bond pool_modified.xlsx",
        header=0,
        encoding="gb2312",
        sheet_name=0,
        index_col=[0, 1],
        parse_dates=True,
    )
    data.to_csv("data.csv", index=None)

    return jsonify("success")


@app.route("/backtest/<nrow>")
def backtest(nrow):
    # should ideally have datetime as index rather then column from source
    target = pd.read_csv(
        "data.csv", header=0, index_col=[0, 1], encoding="gb2312",parse_dates=True, infer_datetime_format=True
    ).iloc[int(nrow), :]
    target_df = pd.DataFrame(pd.to_numeric(target)) # ensure all numeric data
    target_tick = target_df.columns
    target_df.columns = ["Close"]
    target_df["Open"] = target_df["High"] = target_df["Low"] = target_df["Close"] # ensure correct data type
    target_df.index = pd.to_datetime(target_df.index) # ensure datetime index

    bt = Backtest(target_df, SmaCross, cash=10000, commission=0.002)
    result = bt.run()[:-1].to_json()
    # plot = json.dumps(json_item(bt.plot(), 'plot'))
    return jsonify({'result': result})

