# -*- coding: utf-8 -*-

from flask_monitor import ObserverMetrics

import zmq


class ObserverZmq(ObserverMetrics):

    def __init__(self, 
                       context,
                       addr,
                       *args,
                       **kw):
        ObserverMetrics.__init__(self, *args, **kw)
        try:
            self.sock = context.socket(zmq.PUB)
            self.sock.bind(addr)
        except Exception as e:
            self.logger.critical("Cannot connect to ZeroMq '%s'" % str(e))
        

    def action(self, event):
        try:
            self.sock.send(event.json)
        except Exception as e:
            self.logger.critical("Error Unknow on ZeroMq '%s'" % str(e))
            

