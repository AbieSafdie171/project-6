"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
import os
import requests
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
# import config
# from mypymongo import brevet_submit, brevet_display
import logging
import datetime

# *args, **kwargs
###
# Globals
###
app = flask.Flask(__name__)

API_ADDR = os.environ["API_ADDR"]
API_PORT = os.environ["API_PORT"]
API_URL = f"http://{API_ADDR}:{API_PORT}/api"


def brevet_submit(start_time, brevet_dist, controls):
    # inputs into database
    _id = requests.post(f"{API_URL}/brevets",
                        json={"start_time": start_time,
                              "brevet_dist": brevet_dist,
                              "controls": controls}).json()
    return _id


def brevet_display():
    lists = requests.get(f"{API_URL}/brevets").json()

    brevet = lists[-1]

    return brevet["start_time"], brevet["brevet_dist"], brevet["controls"]


###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    br_dist = request.args.get('brevet_distance', 999, type=float)
    br_start_time = request.args.get('brevet_start_time', arrow.now(), type=str)

    app.logger.debug("km={}".format(km))
    app.logger.debug("distance={}".format(br_dist))
    app.logger.debug("start_time={}".format(br_start_time))
    app.logger.debug("request.args: {}".format(request.args))

    input_time = arrow.get(br_start_time).format('YYYY-MM-DDTHH:mm')
    new_input_time = arrow.get(input_time)

    open_time = acp_times.open_time(km, br_dist, new_input_time)
    close_time = acp_times.close_time(km, br_dist, new_input_time)

    close_time = close_time.format('YYYY-MM-DDTHH:mm')
    open_time = open_time.format('YYYY-MM-DDTHH:mm')

    # app.logger.debug("--------OPEN TIME--------")
    # app.logger.debug(open_time)
    # app.logger.debug("--------CLOSE TIME--------")
    # app.logger.debug(close_time)

    result = {"open": open_time, "close": close_time}

    return flask.jsonify(result=result)


@app.route("/display_brevet")
def display_brevet():
    # attempts to fetch data
    try:
        start_time, brevet_dist, controls = brevet_display()
        return flask.jsonify(
            result={"start_time": start_time, "brevet_dist": brevet_dist,
                    "controls": controls},
            status=1,
            message="Successfully fetched a brevet!")
    # throws error message if unsuccessful
    except:
        return flask.jsonify(
            result={},
            status=0,
            message="Something went wrong, couldn't fetch any brevets!")


@app.route("/submit_brevet", methods=['POST'])
def submit_brevet():
    try:
        # Read the entire request body as a JSON
        # This will fail if the request body is NOT a JSON.
        input_json = request.get_json()
        # if successful, input_json is automatically parsed into a python dictionary!

        # Because input_json is a dictionary, we can do this:
        start_time = input_json["start_time"]
        brevet_dist = input_json[
            "brevet_dist"]
        controls = input_json["controls"]

        brevet_id = brevet_submit(start_time, brevet_dist, controls)

        return flask.jsonify(result={},
                             message="Inserted!",
                             status=1,
                             # This is defined by you. You just read this value in your javascript.
                             mongo_id=brevet_id)
    except:
        # The reason for the try and except is to ensure Flask responds with a JSON.
        # If Flask catches your error, it means you didn't catch it yourself,
        # And Flask, by default, returns the error in an HTML.
        # We want /insert to respond with a JSON no matter what!
        return flask.jsonify(result={},
                             message="Oh no! Server error!",
                             status=0,
                             mongo_id='None')


#############

app.debug = os.environ["DEBUG"]
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    app.run(port=os.environ["PORT"], host="0.0.0.0")
