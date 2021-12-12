import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Access the SQLite database
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database into class
Base = automap_base()

# reflect the tables using prepare
Base.prepare(engine, reflect=True)

# measurement and station classes 
Measurement = Base.classes.measurement
Station = Base.classes.station

# session link between Python and database
session = Session(engine)

# create a flask application called 'app'
app = Flask(__name__)

@app.route("/")

def welcome():
    return(
    '''
    Welcome to the Climate Analysis API!
    Available Routes:
    /api/v1.0/precipitation
    /api/v1.0/stations
    /api/v1.0/tobs
    /api/v1.0/temp/start/end
    ''')

@app.route("/api/v1.0/precipitation")

def precipitation():
    # get me all dates from previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query date and precipitation in measurement class
    precipitation = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= prev_year).all()
    # what we want our dictionary to look like 
    # (date is the key/attribute and precipitation is the value)
    precip = {date: prcp for date, prcp in precipitation}
    # give me precip in json format
    return jsonify(precip)

@app.route("/api/v1.0/stations")

def stations():
    # give me all the stations in station class 
    results = session.query(Station.station).all()
    # give me the results as a list of stations
    stations = list(np.ravel(results))
    # give the stations list in  json format
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs")

def temp_monthly():
    # get me all dates from previous year
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query only the temperatures for the station with the most data for the previous year 
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    # give me the relults in a list
    temps = list(np.ravel(results))
    #give the temps in json format
    return jsonify(temps=temps)

#@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)