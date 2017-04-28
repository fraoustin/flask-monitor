# -*- coding: utf-8 -*-
def toflat(obj, ns=""):
    res = {}
    for key in obj:
        if type(obj[key]) is dict:
             subdict =  toflat(obj[key], "%s%s" % (ns,key[0].upper()+key[1:]))
             for k in subdict:
                res[k[0].upper()+k[1:]] = subdict[k]
        else:
            res["%s%s" % (ns, key[0].upper()+key[1:])] = str(obj[key])
    return res

def todict(obj):
    res = {}
    for key in obj:
        if type(obj[key]) is dict:
             subdict =  todict(obj[key])
             for k in subdict:
                res[k] = subdict[k]
        else:
            res[key] = obj[key]
    return res
