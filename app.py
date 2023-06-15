import datetime
import pickle
from eurusdyfinance import *
from flask import Flask, request

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>VLib - Online Library</h1>
                <p>A flask api implementation for book information.   </p>'''

@app.route('/healthpoint', methods=['GET'])
def healthpoint():
    return 'Endpoint is healthy!'


@app.route('/submit', methods=['POST'])
def return_data():
    data = request.get_json()
    format = '%Y-%m-%d'
    fromDate = datetime.strptime(data['fromDate'], format)
    toDate = datetime.strptime(data['toDate'], format)

    return pickle.dumps(execute(fromDate, toDate))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)