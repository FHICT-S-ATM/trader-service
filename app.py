import datetime
import pickle
from eurusdyfinance import *
from flask import Flask, request

app = Flask(__name__)


@app.route('/healthpoint')
def healthpoint():
    return 'Endpoint is healthy!'


@app.route('/submit', methods=['POST'])
def return_data():
    data = request.get_json()
    format = '%Y-%m-%d'
    fromDate = datetime.strptime(data['fromDate'], format)
    toDate = datetime.strptime(data['toDate'], format)

    return pickle.dumps(execute(fromDate, toDate))
