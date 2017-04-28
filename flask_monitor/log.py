# -*- coding: utf-8 -*-

from flask_monitor import ObserverMetrics

class ObserverLog(ObserverMetrics):

    def __init__(self, format="{TimingAsctime} {RequestUrl} {TimingDelta} second(s)", *args, **kw):
        ObserverMetrics.__init__(self, *args, **kw)
        self._format = format

    def action(self, event):
        self.logger.info(self._format.format(**event.flat))

