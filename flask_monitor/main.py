# -*- coding: utf-8 -*-
from time import time, gmtime, asctime
import logging
import json
from flask import current_app, request, Blueprint

from .util import toflat, todict

def everyTrue(event):
    return True

class Event(object):
    
    def __init__(self, response, request, timing):
        self.response = response
        self.request = request
        self.timing = timing
    
    @property
    def _dict(self):
        mydict = {}
        # manage timing
        mydict['timing'] = {}
        mydict['timing']['delta'] = self.timing
        mydict['timing']['start'] = self.request._stats_start_event
        mydict['timing']['asctime'] = asctime(gmtime(self.request._stats_start_event))
        # manage flask
        mydict['flask'] = {}
        mydict['flask']['secret_key'] = current_app.config['SECRET_KEY']
        mydict['flask']['server_name'] = current_app.config['SERVER_NAME']
        mydict['flask']['session_cookie_name'] = current_app.config['SESSION_COOKIE_NAME']
        mydict['flask']['session_cookie_domain'] = current_app.config['SESSION_COOKIE_DOMAIN']
        mydict['flask']['session_cookie_path'] = current_app.config['SESSION_COOKIE_PATH']
        mydict['flask']['session_cookie_httponly'] = current_app.config['SESSION_COOKIE_HTTPONLY']
        mydict['flask']['session_cookie_secure'] = current_app.config['SESSION_COOKIE_SECURE']
        mydict['flask']['session_refresh_each_request'] = current_app.config['SESSION_REFRESH_EACH_REQUEST']
        # manage request
        mydict['request'] = {}
        mydict['request']['url'] = request.url
        mydict['request']['args'] = {arg: request.args.get(arg) for arg in request.args}
        mydict['request']['view_args'] = request.view_args
        mydict['request']['path'] = request.path
        mydict['request']['method'] = request.method
        mydict['request']['remote_addr'] = request.remote_addr
        try:
            mydict['request']['rule'] = request.url_rule.rule
        except:
            mydict['request']['rule'] = ''
        #manage response
        mydict['response'] = {}
        mydict['response']['status_code'] = self.response.status_code
        mydict['response']['headers'] = { i:j for i,j in self.response.headers}
        return mydict                
  
    @property
    def json(self):
        return json.dumps(self._dict)

    @property
    def flat(self):
        return toflat(self._dict) 

    @property
    def dict(self):
        return todict(self._dict)


class EventMetrics(object):
    
    def __init__(self):
        self._obs = []
    
    def __iadd__(self, obs):
        if not callable(obs):
            raise TypeError("objet not callable")
        if obs not in self._obs:
            self._obs.append(obs)
        return self

    def __isub__(self, obs):
        if obs in self._obs:
            self._obs.remove(obs)
        return self

    def __call__(self, *args, **kw):
        [obs(*args, **kw) for obs in self._obs]
        
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# create a singleton for python3
#
# class Metrics(Blueprint, metaclass=Singleton):
#
# for compatible python2, I use module **six**

import six

@six.add_metaclass(Singleton)
class Monitor(Blueprint):

    def __init__(self, *args, **kwargs):
        Blueprint.__init__(self, *args, **kwargs)
        self._event = EventMetrics()
        self.before_app_request(start_event)
        self.after_app_request(stop_event)

    def add_observer(self, obs):
        self._event += obs

    def del_observer(self, obs):
        self._event -= obs

    def add_metric(self, event):
        self._event(event)

class ObserverMetrics(object):

    def __init__(self, filter=everyTrue, logger=None):
        self._filter = filter
        self._logger = logger
    
    @property
    def logger(self):
        if self._logger == None:
            return current_app.logger
        return self._logger

    def __call__(self, event):
        self.logger.debug('intercept event')
        if self._filter(event):
            self.action(event)

    def action(self, event):
        pass


def start_event():
    current_app.logger.debug("start request %s" % request.url)
    request._stats_start_event = time()

def stop_event(response):
    stop = time()
    delta = stop - request._stats_start_event
    current_app.logger.debug("stop request %s" % request.url)
    Monitor().add_metric(Event(response, request, delta))
    return response

