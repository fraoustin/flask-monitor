
from flask import Flask, request, current_app
from flask_monitor import Monitor , ObserverMetrics
from flask_monitor import ObserverLog

import logging

def filterExt(event):
    return event.response.status_code == 400


class myeventlog(ObserverMetrics):

    def __init__(self):
        ObserverMetrics.__init__(self, filter=self.filter)

    def action(self, event):
        logging.getLogger().error(event.json)

    def filter(self, event):
        return event.response.status_code != 400

app = Flask(__name__)
monitor = Monitor('monitor', __name__)
app.register_blueprint(monitor)
#metric.add_observer(myeventlog())
monitor.add_observer(ObserverLog())

#from flask_monitor.influxdb import ObserverInfluxdb
#monitor.add_observer(ObserverInfluxdb(host='127.0.0.1',
#                                    port=8086,
#                                    user='root',
#                                    password='root',
#                                    db='mydb'))

#from flask_monitor.rabbitmq import ObserverRabbit
#import pika

#monitor.add_observer(ObserverRabbit(host='127.0.0.1',
#                            credentials = pika.PlainCredentials('guest', 'guest')))



@app.route("/")
def hello():
    return "Hello World!"

@app.route("/error")
def warning():
    return "error", 400

@app.route('/search')
def search():
    location = request.args.get('location')
    return  location

@app.route('/coucou/<location>')
def coucou(location=None):
    return  location

if __name__ == "__main__":
    app.logger.setLevel(logging.INFO)
    for h in app.logger.handlers:
        h.setLevel(logging.INFO)         
    app.run(port=8080)
