from flask import Flask, jsonify, render_template
from strategy.SmaCross import SmaCross
from backtesting.test import GOOG
from backtesting import Backtest
from bokeh.embed import components
from bokeh.client import pull_session
from bokeh.embed import server_session, json_item
import pandas as pd
import json
from backtesting._plotting import plot
import sys
import re


class Backtest_Graph(Backtest):
    def __init__(self, data, strategy, cash, commission, margin=1, trade_on_close=False):
        super().__init__(data, strategy, cash, commission, margin, trade_on_close)

    def plot(
        self,
        *,
        results: pd.Series = None,
        filename=None,
        plot_width=None,
        plot_equity=True,
        plot_pl=True,
        plot_volume=True,
        plot_drawdown=False,
        smooth_equity=False,
        relative_equity=True,
        omit_missing=True,
        superimpose=True,
        show_legend=True,
        open_browser=True
    ):

        if results is None:
            if self._results is None:
                raise RuntimeError("First issue `backtest.run()` to obtain results.")
            results = self._results

        def _windos_safe_filename(filename):
            if sys.platform.startswith("win"):
                return re.sub(r"[^a-zA-Z0-9,_-]", "_", filename.replace("=", "-"))
            return filename

        return plot(
            results=results,
            df=self._data,
            indicators=results._strategy._indicators,
            filename=filename or _windos_safe_filename(str(results._strategy)),
            plot_width=plot_width,
            plot_equity=plot_equity,
            plot_pl=plot_pl,
            plot_volume=plot_volume,
            omit_missing=omit_missing,
            plot_drawdown=plot_drawdown,
            smooth_equity=smooth_equity,
            relative_equity=relative_equity,
            superimpose=superimpose,
            show_legend=show_legend,
            open_browser=open_browser,
        )


app = Flask(__name__)


# @app.route("/", methods=["GET"])
# def bkapp_page():

#     with pull_session(url="http://localhost:5006/sliders") as session:

#         # update or customize that session
#         session.document.roots[0].children[
#             1
#         ].title.text = "Special Sliders For A Specific User!"

#         # generate a script to load the customized session
#         script = server_session(
#             session_id=session.id, url="http://localhost:5006/sliders"
#         )

#         # use the script in the rendered page
#         return render_template("embed.html", script=script, template="Flask")


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
        "data.csv",
        header=0,
        index_col=[0, 1],
        encoding="gb2312",
        parse_dates=True,
        infer_datetime_format=True,
    ).iloc[int(nrow), :]
    target_df = pd.DataFrame(pd.to_numeric(target))  # ensure all numeric data
    target_tick = target_df.columns
    target_df.columns = ["Close"]
    target_df["Open"] = target_df["High"] = target_df["Low"] = target_df[
        "Close"
    ]  # ensure correct data type
    target_df.index = pd.to_datetime(target_df.index)  # ensure datetime index

    bt = Backtest_Graph(target_df, SmaCross, cash=10000, commission=0.002)
    result = bt.run()
    plot = bt.plot(results=result, filename=None, open_browser=False)
    return json.dumps(json_item(plot, "myplot"))
