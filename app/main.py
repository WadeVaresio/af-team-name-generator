from flask import Flask, request
from pun import compute
import json
import html
from flask.json import jsonify
import random

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route("/generate/non_recursive")
def get_puns():
    user_input = request.args.get('input')

    return jsonify(compute(user_input.split(), 'lev', 10, False, puns=[]))

@app.route("/random_name")
def get_random_name():
    with open('./scrape-data/musicians.txt') as f:
        data = f.readlines()

        chosen = random.choice(data)

        puns = compute(chosen.split(), 'lev', 10, False, puns=[])

        payload = {
            "original": chosen,
            "puns": puns
        }

        return json.dumps(payload)