# -*- coding: utf-8 -*-

from flask_monitor import ObserverMetrics

from influxdb import InfluxDBClient
from influxdb.client import InfluxDBClientError


class ObserverInfluxdb(ObserverMetrics):

    def __init__(self, host, port, user, password, db, measure='flask', *args, **kw):
        ObserverMetrics.__init__(self, *args, **kw)
        self._data = [
            {
                "measurement": measure,
                "tags": {},
                "fields": {},
            }
        ]
        try:
            self.db = InfluxDBClient(host=host,
                                port=port,
                                username=user,
                                password=password,
                                database=db)
        except InfluxDBClientError:
            self.logger.critical("Cannot connect to InfluxDB database '%s'" % db)
        

    def action(self, event):
        try:
            data = self._data
            data[0]['tags'] = event.dict  
            data[0]['fields'] = {"value" : event.timing}
            self.db.write_points(data)
        except InfluxDBClientError as e:
            self.logger.critical("Error InfluxDB '%s'" % str(e))
        except Exception as e:
            self.logger.critical("Error Unknow on InfluxDB '%s'" % str(e))
            

