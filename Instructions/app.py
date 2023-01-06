import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as dt
#database set up
engine=create_engine('sqlite:///Resources/hawaii.sqlite')

Base= automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
measurements=Base.classes.measurement
stations=Base.classes.station

#flask set up
app=Flask(__name__)


@app.route("/")
def welcome():
    '''list possible routes possible for consumer'''
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
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    results = session.query(measurements.date, measurements.prcp).\
        filter(measurements.date>=(dt.date(2017,8,23)-dt.timedelta(days=365))).all()

    session.close()

    # Convert list of tuples into normal list
    prcp_date = []
    for date, prcp in results:
        prcp_name={}
        prcp_name['station']=date
        prcp_name['precipitation']=prcp
        prcp_date.append(prcp_name) 

    return jsonify(prcp_date)

@app.route("/api/v1.0/stations")
def stat():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all stations and names
    results = session.query(stations.station, stations.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_data = []
    for station, name in results:
        stat_name={}
        stat_name['station']=station
        stat_name['name']=name
        station_data.append(stat_name)

    return jsonify(station_data)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all station names"""
    # Query all
    results = session.query(measurements.date, measurements.tobs).\
        filter(measurements.date>(dt.date(2017,8,23)-dt.timedelta(days=365)))\
            .filter(stations.station =='USC00519281').all()

    session.close()

    # Convert list of tuples to something else
    temp_data = []
    for datet, temperature in results:
        temp_name={}
        temp_name['Date']=datet
        temp_name['Temperature']=temperature
        temp_data.append(temp_name)

    return jsonify(temp_data)

@app.route("/api/v1.0/<start_date>$<end_date>")
def start_2(start_date, end_date):
    # '2017-08-16' formart the date should come 
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""
    #connect to database 
    session = Session(engine)

    """Return a list of all station names"""
    # Query all
    sel=[func.min(measurements.tobs),
        func.max(measurements.tobs),
        func.avg(measurements.tobs)
        ]
    results = session.query(*sel).\
        filter(measurements.date>str(start_date)).filter(measurements.date<=end_date).all()

    session.close()

        #once we have results
        #make able to be displayed 
    start_temp_data = []
    for min, max, avg in results:
        temp_name={}
        temp_name['min']=min
        temp_name['max']=max
        temp_name['avg']=avg
        start_temp_data.append(temp_name)

    return jsonify(start_temp_data)

@app.route("/api/v1.0/<start_date>")
def start_end(start_date):
    # '2017-08-16' formart the date should come 
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""
    #connect to database 
    session = Session(engine)

    """Return a list of all station names"""
    # Query all
    sel=[func.min(measurements.tobs),
        func.max(measurements.tobs),
        func.avg(measurements.tobs)
        ]
    results = session.query(*sel).\
        filter(measurements.date>str(start_date)).all()

    session.close()

        #once we have results
        #make able to be displayed 
    start_temp_data = []
    for min, max, avg in results:
        temp_name={}
        temp_name['min']=min
        temp_name['max']=max
        temp_name['avg']=avg
        start_temp_data.append(temp_name)

    return jsonify(start_temp_data)

if __name__ == '__main__':
    app.run(debug=True)