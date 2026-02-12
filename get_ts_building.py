import os
import pandas as pd

HOURLY_RESOLVED = True
# BUILDINGS = ["09.53", "12.01", "13.09", "13.10", "13.53"]
BUILDINGS = ["09.53"]
#TSS = ["WMZ", "KMZ", "ELZ", "Temperatursensor", "RaumTemp", "Windsensor"]
TSS = ["KMZ"]

this_path = os.path.dirname(os.path.abspath(__file__))
building_ts_path = os.path.join(this_path, "raw_data")

for building in BUILDINGS:
    for ts in TSS:
        file_name = building + "_data_export.csv"
        file_path = os.path.join(building_ts_path, file_name)

        # Read CSV into a DataFrame, filtering only rows where "meter name" contains the component_name
        building_data = pd.read_csv(file_path, sep=",")

        # Filter rows where 'meter name' contains the component_name
        prefiltered_df = building_data[building_data["meter_name"].str.contains(ts, na=False)]
        data_names = prefiltered_df["meter_name"].unique()

        for data_name in data_names:
            filtered_df = prefiltered_df[prefiltered_df["meter_name"] == data_name]

            if HOURLY_RESOLVED:
                filtered_df['timestamp_utc'] = pd.to_datetime(filtered_df['timestamp_utc'])
                filtered_df.set_index('timestamp_utc', inplace=True)
                df_hourly = filtered_df["field_value"].resample('H').mean()
                df_hourly = df_hourly.reset_index()
                filtered_df = df_hourly

            if not filtered_df.empty:
                filtered_df.to_csv(os.path.join(this_path, "results", "data", data_name.replace("/", "-") + ".csv"), index=False)
