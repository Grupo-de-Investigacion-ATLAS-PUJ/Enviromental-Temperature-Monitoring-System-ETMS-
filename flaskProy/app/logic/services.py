import plotly.graph_objs as go
import pandas as pd
import numpy as np
from app.data.models import query_data


def create_performance_graph():
    df = query_data()

    # Parse the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])  # Drop rows with invalid time values

    # Clean up the 'name' column to remove prefix and suffix
    df['clean_name'] = df['name'].str.replace(r'^dist_11:ELMB/Can01/ELMB1/AI/', '', regex=True)
    df['clean_name'] = df['clean_name'].str.replace(r'\.value$', '', regex=True)

    # Filter only the first 48 temperature (temperature_0 to temperature_47)
    df = df[df['clean_name'].str.extract(r'(\d+)').astype(int)[0] < 48]

    fig = go.Figure()

    # Group by 'clean_name' to plot each temperature channel with a simplified name
    for name, group in df.groupby('clean_name'):
        fig.add_trace(go.Scatter(
            x=group['time'],
            y=group['original_value_float'],
            mode='lines+markers',
            name=name  # Use the cleaned name for each trace
        ))

    fig.update_layout(
        title='System Performance',
        xaxis_title='Time',
        yaxis_title='temperature (C°)',
        legend_title="temperature Channels"
    )
    
    return fig

def create_trend_graph():
    df = query_data()

    # Parse the 'time' column to datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')
    df = df.dropna(subset=['time'])  # Drop rows with invalid time values

    # Clean up the 'name' column to remove prefix and suffix
    df['clean_name'] = df['name'].str.replace(r'^dist_11:ELMB/Can01/ELMB1/AI/', '', regex=True)
    df['clean_name'] = df['clean_name'].str.replace(r'\.value$', '', regex=True)

    # Filter only the first 48 temperature (temperature_0 to temperature_47)
    df = df[df['clean_name'].str.extract(r'(\d+)').astype(int)[0] < 48]

    # Set the 'time' column as the index for resampling
    df.set_index('time', inplace=True)

    # Resample the data to each second and forward-fill missing values
    resampled_df = df.groupby('clean_name')['original_value_float'].resample('1S').ffill().reset_index()

    # Calculate the average across all sensors for each second
    avg_df = resampled_df.groupby('time')['original_value_float'].mean().reset_index()

    # Plot the average trend over time
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=avg_df['time'],
        y=avg_df['original_value_float'],
        mode='lines',
        name='Average Trend'
    ))

    fig.update_layout(
        title='Average Trend Analysis',
        xaxis_title='Time',
        yaxis_title='Average temperature (C°)',
        legend_title="Trend"
    )

    return fig


# Define alert thresholds
temperature_HIGH_THRESHOLD = 80
temperature_LOW_THRESHOLD = -60

def generate_alerts():
    df = query_data()
    alerts = []

    # Exclude temperature channels 48, 49, 50, and 51
    df = df[~df['name'].str.endswith(('48', '49', '50', '51'))]

    # Check each row for temperature threshold violations
    for _, row in df.iterrows():
        temperature = row['original_value_float']
        sensor_id = row['name']

        if temperature > temperature_HIGH_THRESHOLD:
            alerts.append(f"Sensor {sensor_id} is above the threshold.")
        elif temperature < temperature_LOW_THRESHOLD:
            alerts.append(f"Sensor {sensor_id} is below the threshold.")

    return alerts

