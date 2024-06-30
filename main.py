

import pandas as pd
import requests
from tkinter import *
from tkintermapview import TkinterMapView

API_KEY = "xqZA2rU5Jx4suHs9FAmQy4sUUj4zFPGn"
MIN_LONG = 46.663074
MIN_LAT = 24.516201
MAX_LONG = 46.828239
MAX_LAT = 24.926999

trafficType = {
    0: "Unknown",
    1: "Accident",
    2: "Fog",
    3: "Dangerous Conditions",
    4: "Rain",
    5: "Ice",
    6: "Jam",
    7: "Lane Closed",
    8: "Road Closed",
    9: "Road Works",
    10: "Wind",
    11: "Flooding",
    14: "Broken Down Vehicle"
}

def MarkerAdder(df):
    for _, row in df.iterrows():
        map_widget.set_marker(row['lat'], row['lon'], text=f"{row['type']}")

def DataCleaner(data):
    incidents = data.get("incidents", [])
    incident_list = []

    for incident in incidents:
        incident_type = incident.get('properties', {}).get('iconCategory')
        for cord in incident.get('geometry', {}).get('coordinates', []):
            lat = cord[1]
            lon = cord[0]

            if lat is not None and lon is not None:
                incident_list.append({
                    "lat": lat,
                    "lon": lon,
                    "type": incident_type
                })

    df = pd.DataFrame(incident_list)
    df["type"] = df["type"].map(trafficType)
    MarkerAdder(df)
    print(df)

def save_entry():
    minLonLat = minLongLatEntry.get()
    maxLonLat = maxLongLatEntry.get()

    minLonLatList = minLonLat.split(",")
    maxLonLatList = maxLonLat.split(",")
    IncidentFinder(minLonLatList[0], minLonLatList[1], maxLonLatList[0], maxLonLatList[1], API_KEY)

def IncidentFinder(min_lon, min_lat, max_lon, max_lat, API):
    params = {
        "bbox": f"{min_lon},{min_lat},{max_lon},{max_lat}",
        "key": API
    }
    response = requests.get(url="https://api.tomtom.com/traffic/services/5/incidentDetails", params=params)
    response.raise_for_status()
    data = response.json()
    DataCleaner(data)

# Initialize Map
window = Tk()
window.geometry("1000x1000")
window.title("Traffic Incident Tracker")

# Map Inside Window
map_widget = TkinterMapView(window, width=990, height=500, corner_radius=10)
map_widget.place(relx=0.5, rely=0.3, anchor=CENTER)
map_widget.set_position(24.7136, 46.6753)

# Google URL
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)

# Labels
minLongLatLabel = Label(text="Enter Min Long + Lat:")
minLongLatLabel.place(relx=0.05, rely=0.6)

maxLongLatLabel = Label(text="Enter Max Long + Lat:")
maxLongLatLabel.place(relx=0.05, rely=0.65)

# Entries
entry_text1 = StringVar()
entry_text1.set("Ex: 43,34.5")
entry_text2 = StringVar()
entry_text2.set("Ex: 50,44.5")
minLongLatEntry = Entry(width=30, textvariable=entry_text1)
minLongLatEntry.place(relx=0.2, rely=0.6)

maxLongLatEntry = Entry(width=30, textvariable=entry_text2)
maxLongLatEntry.place(relx=0.2, rely=0.65)

# Buttons
trafficButton = Button(text="Find Incidents!", command=save_entry)
trafficButton.place(relx=0.2, rely=0.7)

window.mainloop()
