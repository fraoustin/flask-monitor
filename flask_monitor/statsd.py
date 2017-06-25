# -*- coding: utf-8 -*-

from flask_monitor import ObserverMetrics

import statsd


class ObserverStatsd(ObserverMetrics):

    args_statsd = ['host', 'port', 'prefix', 'maxudpsize', 'ipv6']
    
    def __init__(self,format="flask", 
                       *args,
                       **kw):
        kw_statsd = { key : kw[key] for key in kw if key in self.args_statsd}
        kw = { key : kw[key] for key in kw if key not in self.args_statsd}
        ObserverMetrics.__init__(self, *args, **kw)
        self._format = format
        try:
            
            self.client = statsd.StatsClient(**kw_statsd)
        except Exception as e:
            self.logger.critical("Cannot connect to Statsd '%s'" % str(e))
        

    def action(self, event):
        try:
            self.client.timing(self._format.format(**event.flat), event.timing)
        except Exception as e:
            self.logger.critical("Error Unknow on Statsd '%s'" % str(e))
            

