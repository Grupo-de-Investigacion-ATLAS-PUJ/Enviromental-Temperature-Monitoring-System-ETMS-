
from flask import Blueprint, render_template,jsonify
from app.logic.services import create_performance_graph, create_trend_graph
from app.logic.services import generate_alerts
from app.data.models import get_sensor_info
import plotly.io as pio

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', page_id="dashboard")

sensor_coordinates = [{'coords': '205,103,15'}, {'coords': '235,86,12'}, {'coords': '261,74,12'}, {'coords': '452,121,12'}, {'coords': '553,103,12'}, {'coords': '429,142,12'}, {'coords': '460,149,12'}, {'coords': '525,88,12'}, {'coords': '463,726,12'}, {'coords': '494,716,12'}, {'coords': '523,704,15'}, {'coords': '298,641,14'}, {'coords': '86,571,12'}, {'coords': '71,540,14'}, {'coords': '253,417,15'}, {'coords': '253,375,15'}, {'coords': '74,333,14'}, {'coords': '418,546,16'}, {'coords': '681,463,15'}, {'coords': '501,414,15'}, {'coords': '502,375,16'}, {'coords': '359,273,15'}, {'coords': '441,569,15'}, {'coords': '43,338,14'}, {'coords': '50,309,14'}, {'coords': '60,280,12'}, {'coords': '71,249,14'}, {'coords': '86,221,12'}, {'coords': '292,64,12'}, {'coords': '285,96,12'}, {'coords': '315,88,14'}, {'coords': '435,58,16'}, {'coords': '466,64,14'}, {'coords': '670,222,12'}, {'coords': '686,250,14'}, {'coords': '698,278,14'}, {'coords': '705,309,11'}, {'coords': '714,341,12'}, {'coords': '714,452,12'}, {'coords': '707,481,14'}, {'coords': '697,513,14'}, {'coords': '684,541,14'}, {'coords': '669,569,12'}, {'coords': '432,732,12'}, {'coords': '471,693,15'}, {'coords': '442,701,14'}, {'coords': '292,725,12'}, {'coords': '261,715,12'}]

@views.route('/variables')
def variables():
    sensor_info = get_sensor_info()  # Obtén la información desde InfluxDB
    # Combina coordenadas y datos de sensores en una sola lista
    sensors = [
        {**info, **coord}
        for info, coord in zip(sensor_info, sensor_coordinates)
    ]
    return render_template('variables.html', sensors=sensors, page_id="variables")

@views.route('/alerts')
def alerts():
    return render_template('alerts.html', page_id="alerts")

@views.route('/reports')
def reports():
    return render_template('reports.html', page_id="reports")

@views.route('/settings')
def settings():
    return render_template('settings.html', page_id="settings")

@views.route('/api/performance_data')
def get_performance_data():
    performance_graph = create_performance_graph()
    return jsonify(pio.to_json(performance_graph))

@views.route('/api/trend_data')
def get_trend_data():
    trend_graph = create_trend_graph()
    return jsonify(pio.to_json(trend_graph))

@views.route('/api/alerts')
def get_alerts():
    # Return the generated alerts in JSON format
    alerts = generate_alerts()
    return jsonify(alerts)
