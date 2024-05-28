#Install Flask
pip install flask

from flask import Flask, jsonify
import pandas as pd

# Read the CSV files into DataFrames
stations_df = pd.read_csv("/Users/lisashimano/Documents/UWA Data Analytics Bootcamp/sqlalchemy-challenge/Starter_Code 4/Resources/hawaii_stations.csv")
measurements_df = pd.read_csv("/Users/lisashimano/Documents/UWA Data Analytics Bootcamp/sqlalchemy-challenge/Starter_Code 4/Resources/hawaii_measurements.csv")

# Convert the 'date' column to datetime format
measurements_df['date'] = pd.to_datetime(measurements_df['date'])

app = Flask(__name__)

# Helper function to calculate temperature stats
def calc_temps(start_date, end_date=None):
    if end_date:
        data = measurements_df[(measurements_df['date'] >= start_date) & (measurements_df['date'] <= end_date)]
    else:
        data = measurements_df[measurements_df['date'] >= start_date]

    TMIN = data['tobs'].min()
    TAVG = data['tobs'].mean()
    TMAX = data['tobs'].max()
    return TMIN, TAVG, TMAX

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the dataset
    latest_date = measurements_df['date'].max()
    one_year_ago = latest_date - pd.DateOffset(years=1)

    # Filter the data for the last 12 months
    last_12_months = measurements_df[(measurements_df['date'] >= one_year_ago) & (measurements_df['date'] <= latest_date)]
    
    # Convert to dictionary
    prcp_data = last_12_months[['date', 'prcp']].set_index('date').to_dict()['prcp']
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    stations_list = stations_df['station'].tolist()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most recent date in the dataset
    latest_date = measurements_df['date'].max()
    one_year_ago = latest_date - pd.DateOffset(years=1)

    # Find the station with the most observations
    most_active_station_id = measurements_df['station'].value_counts().idxmax()

    # Filter the data for the last 12 months for the most-active station
    tobs_last_12_months = measurements_df[(measurements_df['station'] == most_active_station_id) &
                                          (measurements_df['date'] >= one_year_ago) &
                                          (measurements_df['date'] <= latest_date)]

    tobs_data = tobs_last_12_months['tobs'].tolist()
    return jsonify(tobs_data)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    try:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end) if end else None
    except Exception as e:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    TMIN, TAVG, TMAX = calc_temps(start_date, end_date)
    temp_stats = {
        "TMIN": TMIN,
        "TAVG": TAVG,
        "TMAX": TMAX
    }
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)

python app.py