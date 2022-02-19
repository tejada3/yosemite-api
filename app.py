from urllib.error import HTTPError
# This is a sample Python script.
from urllib.request import urlopen

import boto3
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_restful import Api
from DayToDay import *

app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
BASE_ROUTE = "/weather"
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')


def print_hi(url):
    title = None
    try:

        html = urlopen(url)

    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html.read(), 'html.parser')
        title = bs
        return title
    except AttributeError as e:
        print(e)

    return title


@app.route(BASE_ROUTE + "/yosemite-valley", methods=['GET'])
def yosemiteValley():  # put application's code here
    yvTemp = print_hi("https://forecast.weather.gov/MapClick.php?lon=-119.61292&lat=37.73639#.YgvkjejMIuV")
    temp = yvTemp.html.body.find('p', {'class': 'myforecast-current-lrg'}).getText().strip("°F")
    print(temp)
    return temp


@app.route(BASE_ROUTE + "/tuolumne-meadows", methods=['GET'])
def tuolumneMeadows():
    tmTemp = print_hi("https://forecast.weather.gov/MapClick.php?lon=-119.35666&lat=37.87522#.Ygvo2ujMIuV")
    temp = tmTemp.html.body.find('p', {'class': 'myforecast-current-lrg'}).getText().strip("°F")
    return temp


@app.route(BASE_ROUTE + "/mariposa-grove", methods=['GET'])
def mariposaGrove():
    mgTemp = print_hi("https://forecast.weather.gov/MapClick.php?lon=-119.60039&lat=37.50387#.YgvqX-jMIuV")
    temp = mgTemp.html.body.find('p', {'class': 'myforecast-current-lrg'}).getText().strip("°F")
    return temp


@app.route(BASE_ROUTE + "/DayToDay", methods=['POST'])
def dayToday():
    e = Event(order=1, event="GET THERE SAFTLY")

    d2d = DaytoDay(trip="Yosemite",
                   dayOne=[{"order": e.order,
                            "event": e.event}],
                   dayTwo=[{"order": e.order,
                            "event": e.event}],
                   dayThree=[{"order": e.order,
                            "event": e.event}],
                   dayFour=[{"order": e.order,
                            "event": e.event}],
                   dayFive=[{"order": e.order,
                            "event": e.event}])

    table = dynamodb.Table(d2d.Meta.table_name)

    response = table.put_item(
        Item={
            "trip": d2d.trip,
            "dayOne": d2d.dayOne,
            "dayTwo": d2d.dayOne,
            "dayThree": d2d.dayOne,
            "dayFour": d2d.dayOne,
            "dayFive": d2d.dayOne,
        }
    )
    print(d2d.dayOne)
    print(response)
    return jsonify({"Message": "Successfully added",
                    "response": response}), 201


@app.route(BASE_ROUTE + "/DayToDay", methods=['GET', 'PUT'])
def AddEvent():
    data = request.json

    table = dynamodb.Table("DayToDay")
    try:
        response = table.get_item(
            Key={
                'trip': "Yosemite",
            }
        )
        print(response["Item"][data["day"]])
        i = response["Item"][data["day"]]
        print(len(i))

        newEvent = {
        "order": len(response["Item"][data["day"]]) + 1,
        "event": data["message"]
    }
        hereitis = table.update_item(
            Key={
                'trip': "Yosemite",
            },
            UpdateExpression='SET #{} = list_append({}, :tempval)'.format(data['day'], data['day']),
            ExpressionAttributeNames={
                '#{}'.format(data['day']): '{}'.format(data['day'])
            },
            ExpressionAttributeValues={
                ':tempval': [newEvent]
            },
        )

        return jsonify({"data": hereitis})



    except Exception as a:
        print(a)
        return jsonify({"message": str(a)})


if __name__ == '__main__':
    app.run()
