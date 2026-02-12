import os
import pandas as pd
import plotly.express as px
import plotly.io as pio


def get_ts_to_be_plotted(ts_name):
    if "KMZ" in ts_name:
        return "Cooling demand in kWh"
    elif "WMZ" in ts_name:
        return "Heat demand in kWh"
    elif "ELZ" in ts_name:
        return "Electrical demand in kWh"
    elif "Temperatursensor" in ts_name:
        return "Temperature in °C"
    elif "RaumTemp" in ts_name:
        return "Room Temperature in °C"
    elif "Windsensor" in ts_name:
        return "Windspeed in m/s or Wind direction DEGREES_ANGULAR"


this_path = os.path.dirname(os.path.abspath(__file__))
building_tss_path = os.path.join(this_path, "results", "data")
save_dir = os.path.join(this_path, "results", "plots")
os.makedirs(save_dir, exist_ok=True)

for building_ts_file_name in os.listdir(building_tss_path):
    if not building_ts_file_name.endswith(".csv"):
        continue  # skip non-csv files

    building_ts_name = os.path.splitext(building_ts_file_name)[0]
    building_ts_path = os.path.join(building_tss_path, building_ts_file_name)
    building_ts = pd.read_csv(building_ts_path, sep=",")

    # Get value label
    ts = get_ts_to_be_plotted(building_ts_name) or "Value"

    # Convert timestamp
    building_ts['timestamp_utc'] = pd.to_datetime(building_ts['timestamp_utc'])

    # Create interactive plot
    fig = px.line(
        building_ts,
        x='timestamp_utc',
        y='field_value',
        title=f'Time series of: {building_ts_name}',
        labels={'timestamp_utc': 'Date', 'field_value': ts},
    )

    fig.update_layout(xaxis_title='Date', yaxis_title=ts)
    fig.update_traces(mode='lines+markers')

    # Save as HTML
    html_path = os.path.join(save_dir, f"{building_ts_name}.html")
    pio.write_html(fig, file=html_path, auto_open=False)

    print(f"Interactive plot saved to: {html_path}")
