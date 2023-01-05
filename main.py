# import of the modules
from flask import Flask, render_template
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import requests
import lxml
import pandas as pd
from pytrends.request import TrendReq


app = Flask(__name__)


# print Hello World on the home page
@app.route('/', methods=["GET"])
def hello_world():
    prefix_google = """
    <!-- Google tag (gtag.js) -->
    <script async
    src="https://www.googletagmanager.com/gtag/js?id=UA-251003635-1"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', ' UA-251003635-1');
    </script>
    """
    return prefix_google + "Hello World"


# add a route to print some logs
@app.route('/logger', methods=["GET"])
def logger():
    script = """
    <script> console.log("This is a log in the console")</script>"""
    return "This is a log :)" + script


# add a route to print the user input in the console from the textbox
@app.route('/textbox', methods=["GET"])
def print():
    script = """
    <script>
        function myFunction() {
        var message = document.getElementById("message").value;
        console.log(message);
        }
    </script>"""
    return """
    <input type="text" id="message" placeholder="Enter a message">
    <button onclick="myFunction()">Print</button>""" + script



@app.route('/cookies/', methods = ["GET"])
def req():
    #req = requests.get("https://www.google.com/")
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251003635w345024245p281152693")
    
    # return req.cookies.get_dict()
    return req.text




SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'digital-traces-373513-1489f264a109.json'
VIEW_ID = '281152693' #You can find this in Google Analytics > Admin > Property > View > View Settings (VIEW ID)


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
        }]
      }
  ).execute()


def get_visitors(response):
    visitors = 0 # in case there are no analytics available yet
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dateRangeValues = row.get('metrics', [])

            for i, values in enumerate(dateRangeValues):
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    visitors = value

    return str(visitors)


@app.route('/visitors')
def visitors():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    visitors = get_visitors(response)

    # return render_template('visitors.html', visitors=str(visitors))
    return "nombre de visiteurs : "+visitors


@app.route('/trends')
def chart():
    trend_dict = get_trend_data()   
    return render_template('index_chart.html', trend_data=trend_dict)

def get_trend_data():
    pytrend = TrendReq()

    kw_list = ['vacances', 'soleil']
    pytrend.build_payload(kw_list)
    trend_data = pytrend.interest_over_time()
    trend_dict = trend_data.to_dict(orient='records')

    return trend_dict

if __name__ == '__main__':

    app.run(debug=True)
