import config
from influxdb import InfluxDBClient
import pandas as pd

# InfluxDB client setup using credentials
client = InfluxDBClient(
    host=config.INFLUXDB_HOST,
    port=config.INFLUXDB_PORT,
    username=config.INFLUXDB_USER,
    password=config.INFLUXDB_PASSWORD,
    database=config.INFLUXDB_DATABASE
)

def query_data():
    query = "SELECT * FROM EVENT.EVENT WHERE variabletype='FwElmbAi' AND time > now() - 15s"
    result = client.query(query)
    
    df = pd.DataFrame(list(result.get_points()))
    
    if df.empty:
        print("No data available for the specified query.")
        return pd.DataFrame(columns=['time', 'name', 'original_value_float'])
    
    # Return the relevant columns: time, name, and original_value_float
    return df[['time', 'name', 'original_value_float']]

client2 = InfluxDBClient(
    host=config.INFLUXDB_HOST,
    port=config.INFLUXDB_PORT,
    username=config.INFLUXDB_USER,
    password=config.INFLUXDB_PASSWORD,
    database="sensors_data"
)


def get_sensor_info():
    query2 = "SELECT * FROM sensor_info"
    result = client2.query(query2)
    return list(result.get_points())