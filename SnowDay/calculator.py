from processor import getSummary, getLong, getLat, getType, getSpeed, getTemp, getPrecipChance, getTime, getAccumulation
import json
import numpy
import pandas
import sklearn

def weighTime():
    if(getTime()>20 or getTime()<5):
        return 1
    else:
        return 0

def weighPrecipChance():
    return getPrecipChance()*100

def weighTemp():
    return True

def weighSpeed():
    return True

def weighType():
    return True

def weighProbability():
    return True

def weighAccumulation():
    return True

