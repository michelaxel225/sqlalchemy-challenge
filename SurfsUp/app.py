import numpy as np
import sqlalchemy
import datetime as dt 
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify




# database set up and creation of the engine 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
base.classes.keys()

# Save reference to the table
measurement = base.classes.measurement
station = base.classes.station

# Create Session  From Python to the DB
session = Session(engine)

# app set up 
app = Flask(__name__)
#flask route 
@app.route("/")
def Homepage():
     return (
        'Available Routes: <br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'Please enter date in this format YYYY-MM-DD<br/>'
        f'/api/v1.0/start_date$end_date<br/>'
        f'/api/v1.0/start_date'
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
previous_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= previous_year).all()  
precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)
   

@app.route("/api/v1.0/stations")
def stations():
    global station
    session = Session(engine)
    results = session.query(station.id, station.station,station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    stations= []
    for id, station, name, latitude, longitude, elevation in results2:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results2 = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.station == 'USC00519281').all()
    session.close()

    tobs = []
    for date,tobs in results2:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results3 = session.query(measurement.date,
                            func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()
    session.close()

    starts = []
    for date, minimum, mean, maximum in results3:
        start_dict = {}
        start_dict["date"] = start
        start_dict["minimum"] = minimum
        start_dict["mean"] = mean
        start_dict["maximum"] = maximum
        start_list.append(start_dict)
    return jsonify(starts)




@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
   
    session = Session(engine)
    results4 = session.query(measurement.date,
                            func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                filter(measurement.date >= start).\
                filter(measurement.date < end).all()
    session.close()


   ends = []
    for date,minimum,mean,maximum in results4:
        startend_dict = {}
        startend_dict["startdate"] = start
        startend_dict["enddate"] = end
        startend_dict["minimum"] = minimum
        startend_dict["mean"] = mean
        startend_dict["maximum"] = maximum
        startend_list.append(startend_dict)
    return jsonify(ends)



if __name__ == '__main__':
    app.run(debug=True)