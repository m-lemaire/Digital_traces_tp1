# import of the modules
from flask import Flask, render_template
import requests


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

<<<<<<< HEAD
@app.route('/cookies/', methods = ["GET"])
def req():
    #req = requests.get("https://www.google.com/")
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251003635w345024245p281152693")
    
    # return req.cookies.get_dict()
    return req.text

if __name__ == '__main__':

    app.run(debug=True)
=======

if __name__ == '__main__':

    app.run(debug=True)
>>>>>>> 90b73ba45e942f586a673100cc40dee94e9b04f6
