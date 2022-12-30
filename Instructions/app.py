import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


##################### database set up ####################

# database set up
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save reference to the table
measurement = Base.classes.measurement
station = Base.classes.station

# Create Session  From Python to the DB
session = Session(engine)

####################### flack set up ######################
app = Flask(__name__)

####################### flack routes ######################
# * `/`
#     * Homepage.
#     * List all available routes.
@app.route("/")
def Homepage():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/yyyy-mm-dd<br/>"
        f"/api/v1.0/yyyy-mm-dd/yyyy-mm-dd"
    )



# * `/api/v1.0/precipitation`
#     * Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
#     * Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(measurement.date, measurement.prcp).all()
    session.close()

    measurement_list = []
    for key,value in results:
        measurement_dict = {key : value}
        measurement_list.append(measurement_dict)
    return jsonify(measurement_list)




# * `/api/v1.0/stations`
#     * Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    global station
    session = Session(engine)
    results2 = session.query(station.id, station.station,station.name, station.latitude, station.longitude, station.elevation).all()
    session.close()

    station_list = []
    for id, station, name, latitude, longitude, elevation in results2:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = latitude
        station_dict["longitude"] = longitude
        station_dict["elevation"] = elevation
        station_list.append(station_dict)
    return jsonify(station_list)



# * `/api/v1.0/tobs`
#     * Query the dates and temperature observations of the most active station for the previous year of data.
#     * Return a JSON list of temperature observations (TOBS) for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results3 = session.query(measurement.date, measurement.tobs).\
    filter(measurement.date >= '2016-08-23').\
    filter(measurement.station == 'USC00519281').all()
    session.close()

    tobs_list = []
    for date,tobs in results3:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)
    return jsonify(tobs_list)





# * `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
#     * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a given start or start-end range.
#     * When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than or equal to the start date.
#     * When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates from the start date through the end date (inclusive).




@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    results4 = session.query(measurement.date,
                            func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                filter(measurement.date >= start).all()
    session.close()

    start_list = []
    for date, minimum, mean, maximum in results4:
        start_dict = {}
        start_dict["date"] = start
        start_dict["minimum"] = minimum
        start_dict["mean"] = mean
        start_dict["maximum"] = maximum
        start_list.append(start_dict)
    return jsonify(start_list)




@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):
   
    session = Session(engine)
    results5 = session.query(measurement.date,
                            func.min(measurement.tobs),
                            func.avg(measurement.tobs),
                            func.max(measurement.tobs)).\
                filter(measurement.date >= start).\
                filter(measurement.date < end).all()
    session.close()


    startend_list = []
    for date,minimum,mean,maximum in results5:
        startend_dict = {}
        startend_dict["startdate"] = start
        startend_dict["enddate"] = end
        startend_dict["minimum"] = minimum
        startend_dict["mean"] = mean
        startend_dict["maximum"] = maximum
        startend_list.append(startend_dict)
    return jsonify(startend_list)






####################### Define main behavior ######################
if __name__ == '__main__':
    app.run(debug=True)