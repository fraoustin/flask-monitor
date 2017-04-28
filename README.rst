Flask-monitor
=============

Generate time of execution and send data on multi destination

- log
- influxdb (and so grafana)
- rabbitmq
- zeromq
- statsd


Installation
------------

::

    pip install flask-monitor
        
Or

::

    git clone https://github.com/fraoustin/flask-monitor.git
    cd flask-monitor
    python setup.py install

Usage
-----


::

    from flask import Flask, request
    from flask_monitor import Monitor , ObserverLog
    import logging

    app = Flask(__name__)
    monitor = Monitor('monitor', __name__)
    app.register_blueprint(monitor)
    monitor.add_observer(ObserverLog())

    @app.route("/")
    def hello():
        return "Hello World!"

    if __name__ == "__main__":
        app.logger.setLevel(logging.INFO)
        for h in app.logger.handlers:
            h.setLevel(logging.INFO)         
        app.run(port=8080)

You can add a filter of event

::

    from flask import Flask, request
    from flask_monitor import Monitor , ObserverLog
    
    def filterExt(event):
        return event.response.status_code == 400

    app = Flask(__name__)
    monitor = Monitor('monitor', __name__)
    app.register_blueprint(monitor)
    monitor.add_observer(ObserverLog(filter=filterExt))

    @app.route("/")
    def hello():
        return "Hello World!"

    if __name__ == "__main__":
        app.run(port=8080)


You can create your own observer

::

    from flask import Flask, request
    from flask_monitor import Monitor , ObserverLog
     
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
    monitor.add_observer(myeventlog())

    @app.route("/")
    def hello():
        return "Hello World!"

    if __name__ == "__main__":
        app.run(port=8080)


Influxdb
--------

::

    pip install influxdb

Usage

::

    from flask_monitor.influxdb import ObserverInfluxdb
    monitor.add_observer(ObserverInfluxdb(host='127.0.0.1',
                                        port=8086,
                                        user='root',
                                        password='root',
                                        db='mydb'))

RabbitMq
--------

::

    pip install pika

Usage

::

    from flask_monitor.rabbitmq import ObserverRabbit
    import pika

    monitor.add_observer(ObserverRabbit(host='127.0.0.1',
                                credentials = pika.PlainCredentials('guest', 'guest')))

ZeroMq
------

::

    pip install zmq

Usage

::

    from flask_monitor.zeromq import ObserverZmq
    import zmq

    monitor.add_observer(ObserverZmq(context=zmq.Context(),
                                        addr='tcp://127.0.0.1:8080'))

Statsd
------

::

    pip install statsd

Usage

::

    from flask_monitor.statsd import ObserverStatsd
    monitor.add_observer(ObserverStatsd(host='127.0.0.1', port=8125, format="{RequestUrl}"))
    

