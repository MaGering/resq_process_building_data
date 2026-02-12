import pandas as pd
import os

this_path = os.path.dirname(os.path.abspath(__file__))
building_tss_path = os.path.join(this_path, "results", "data")

for building_ts_file_name in os.listdir(building_tss_path):
    if "Energie" in building_ts_file_name:
        if building_ts_file_name.replace("Energie", "Leistung") not in os.listdir(building_tss_path):
            if not building_ts_file_name.endswith(".csv"):
                continue  # skip non-csv files

            building_ts_name = os.path.splitext(building_ts_file_name)[0]
            building_ts_path = os.path.join(building_tss_path, building_ts_file_name)
            building_ts = pd.read_csv(building_ts_path, sep=",", parse_dates=["timestamp_utc"])
            building_ts = building_ts.sort_values("timestamp_utc")

            # Berechne Differenz (ΔE) und wandle in kW um
            building_ts["delta_mwh"] = building_ts["field_value"].diff()
            building_ts["field_value"] = building_ts["delta_mwh"] * 1000

            # Entferne Hilfsspalte
            building_ts.drop(columns=["delta_mwh"], inplace=True)

            # Neuen Dateinamen erzeugen
            capacity_file_name = building_ts_file_name.replace("Energie", "Leistung")
            capacity_file_path = os.path.join(building_tss_path, capacity_file_name)

            # Als CSV speichern
            building_ts.to_csv(capacity_file_path, sep=",", index=False)