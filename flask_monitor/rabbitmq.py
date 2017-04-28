# -*- coding: utf-8 -*-

from flask_monitor import ObserverMetrics

import pika


class ObserverRabbit(ObserverMetrics):

    args_mq = ['host','port','virtual_host','credentials','channel_max','frame_max',
                'heartbeat', 'ssl', 'ssl_options', 'connection_attempts', 'retry_delay',
                'socket_timeout', 'locale', 'backpressure_detection', 'blocked_connection_timeout',
                'client_properties']
    
    def __init__(self, 
                       exchange='flask',
                       routing_key='',
                       *args,
                       **kw):
        kw_mq = { key : kw[key] for key in kw if key in self.args_mq}
        kw = { key : kw[key] for key in kw if key not in self.args_mq}
        ObserverMetrics.__init__(self, *args, **kw)
        try:
            
            connection = pika.BlockingConnection(pika.ConnectionParameters(**kw_mq))
            self.channel = connection.channel()
            self.exchange = exchange
            self.routing_key = routing_key
            try:
                self.channel.exchange_declare(exchange=exchange,
                                               type='fanout')
                self.logger.debug("Create channel RabbitMq '%s'" % exchange)
            except:
                self.logger.debug("Not create channel RabbitMq '%s'" % exchange)
        except Exception as e:
            self.logger.critical("Cannot connect to RabbitMq '%s'" % str(e))
        

    def action(self, event):
        try:
            self.channel.basic_publish(exchange=self.exchange,
                                  routing_key=self.routing_key,
                                  body=event.json)
        except Exception as e:
            self.logger.critical("Error Unknow on RabbitMq '%s'" % str(e))
            

