import argparse
import datetime
import json
import sys

from dateutil.parser import parse as dateparse
import flask as f
import hammers

import queries


app = f.Flask(__name__)
db = None


def isoify_dates(data):
    for element in data:
        for key in element:
            if isinstance(element[key], datetime.datetime):
                element[key] = element[key].isoformat()


@app.route("/events/daterange", methods=['GET', 'POST'])
def events_by_date():
    if f.request.method == 'POST':
        from_date = dateparse(f.request.json['from'])
        to_date = dateparse(f.request.json['to'])
        data = list(queries.events_date_range(db, from_date, to_date))
        isoify_dates(data)
        return f.jsonify(data)
    else:
        return 'POST a JSON object here with "from" and "to" keys in a date format.'


@app.route("/events/afterid", methods=['GET'])
def events_by_id_info():
    return 'GET from /events/afterid/<int> with the number being the first event_id to return, up to 1000 records.'


@app.route("/events/afterid/<int:first_id>", methods=['GET'])
def events_by_id(first_id):
    data = list(queries.events_after_id(db, first_id))
    isoify_dates(data)
    return f.jsonify(data)


def main(argv=None):
    global db

    if argv is None:
        argv = sys.argv

    mysqlargs = hammers.MySqlArgs({
        'user': 'readonly',
        'password': '',
        'host': '127.0.0.1',
        'port': 3306,
    })
    parser = argparse.ArgumentParser()
    mysqlargs.inject(parser)

    args = parser.parse_args(argv[1:])
    mysqlargs.extract(args)

    db = mysqlargs.connect()

    app.run()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
