from flask import Flask, jsonify, render_template
from strategy.SmaCross import SmaCross
from backtesting.test import GOOG
from backtesting import Backtest
from bokeh.embed import components
from bokeh.client import pull_session
from bokeh.embed import server_session

app = Flask(__name__)

@app.route('/', methods=['GET'])
def bkapp_page():

    with pull_session(url="http://localhost:5006/sliders") as session:

        # update or customize that session
        session.document.roots[0].children[1].title.text = "Special Sliders For A Specific User!"

        # generate a script to load the customized session
        script = server_session(session_id=session.id, url='http://localhost:5006/sliders')

        # use the script in the rendered page
        return render_template("embed.html", script=script, template="Flask")


# @app.route('/')
# def hello_world():
#     return 'Hello, World!'

@app.route('/test')
def test_goog():
    bt = Backtest(GOOG, SmaCross, cash=10000, commission=.002)
    result = bt.run()[:-1].to_json()
    return result

@app.route('/visual')
def visual():
    bt = Backtest(GOOG, SmaCross, cash=10000, commission=.002)
    bt.run()
    plot = bt.plot() 
    script, div = components(plot)
    return render_template("visual.html", script=script, div=div)