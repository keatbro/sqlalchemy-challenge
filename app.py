import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
measurements = Base.classes.measurement
stations = Base.classes.station

# Flask setup
app = Flask(__name__)

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    f"Return a JSON object of all precipitation measurements and dates."
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all precipitation
    results = session.query(measurements.date, measurements.prcp).all()
    
    precipitation = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        precipitation.append(prcp_dict)
    session.close()

    # Convert list of tuples into normal list
    data = list(np.ravel(results))

    return jsonify(data)

@app.route("/api/v1.0/stations")
def stationsFunc():
    f"Returns a JSON object of all stations."
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all stations
    results = session.query(stations.station, stations.name).all()

    # Convert list of tuples into normal list
    data = list(np.ravel(results))

    return jsonify(data)

@app.route("/api/v1.0/tobs")
def tobsFunc():
    f"Returns the last year of measurement data."

    # Trying out Pandas instead because it's much more straightforward.
    df = pd.read_sql('select date, tobs from measurement where date between "2016-08-23" and "2017-08-23" group by 1 order by date desc', engine)

    # Use to_json function to return dataframe as JSON object.
    return df.to_json(orient='table')

@app.route("/api/v1.0/<start_date>")
def startFunc(start_date):
    f"Returns the average, max and min temperature for all dates greater than a specified date."
    
    # Trying out Pandas instead because it's much more straightforward.
    df = pd.read_sql(f"select avg(tobs), max(tobs), min(tobs) from measurement where date >= '{start_date}'", engine)

    # Use to_json function to return dataframe as JSON object.
    return df.to_json()

@app.route("/api/v1.0/<start_date>/<end_date>")
def startEndFunc(start_date, end_date):
    f"Returns the average, max and min temperature for a specified date."
    
    # Trying out Pandas instead because it's much more straightforward.
    df = pd.read_sql(f"select avg(tobs), max(tobs), min(tobs) from measurement where date <= '{start_date}' and date <= '{end_date}'", engine)

    # Use to_json function to return dataframe as JSON object.
    return df.to_json()

if __name__ == '__main__':
    app.run(debug=True)
