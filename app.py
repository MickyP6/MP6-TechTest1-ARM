from flask import Flask, Response, render_template

import data_cleanser
from get_google_data import GoogleApiRequest

app = Flask(__name__)


@app.route('/')
def index():
    """
    This routes the base url to index.html from static file.
    """
    return render_template('index.html')


@app.route("/grab_data")
def grab_data() -> Response:
    """
    This is the main entrypoint for d3 to request data.
    """
    data = GoogleApiRequest().request_data()
    data = data_cleanser.jsonify_data(data)

    return Response(data, mimetype='application/json')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
