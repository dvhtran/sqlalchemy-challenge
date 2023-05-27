# Import the dependencies.

import numpy as np
import datetime as dt 

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 

#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model

Base = automap_base() 

# reflect the tables

Base.prepare(engine, reflect=True)

# Save references to each table

Measurement = Base.classes.measurement
Station = Base.classes.station 


# Create our session (link) from Python to the DB

session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    return (
        "Welcome to the SQL-Alchemy APP API!<br/>"
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        "/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )
if __name__=="__main__":
    print(welcome())
    
    

#Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= query_date).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

#Stations route
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(stations.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

#Tobs route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    query_date = dt.date(2017,8,23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.stations == 'USC00519281').\
        filter(Measurement.date >= query_date).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

#Statistics Route
@app.route("/api/v1.0/temp<start>")
@app.route("/api/v1.0/temp/<start>/<end>")

def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= end).all()
        temps = list(np.ravel(results))
        return jsonify(temps)   
    
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

if __name__== "__main__":
    app.run()
