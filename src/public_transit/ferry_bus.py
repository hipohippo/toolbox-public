import pandas as pd
import requests

unix_now = pd.Timestamp.now().timestamp()
result = requests.get(
    "https://services.saucontds.com/tds-map/nyw/nywvehiclePositions.do?", params={"id": 93, "time": unix_now}
)
conversion = requests.get("https://services.saucontds.com/tds-map/nyw/nywmapTranslation.do?id=93")
conversion = conversion.json()


class COORD:
    COORD_50_5 = (40.758547, -73.977167)
    COORD_50_6 = 40.759859, -73.980451
    COORD_50_7 = 40.761089, -73.983248
    COORD_50_8 = (40.762264, -73.986099)


if result.status_code == 200:
    buses = result.json()
    for bus in buses:
        ordx = (bus["x"] - 0.5) * conversion["mapConversionX"] + conversion["mapBoundsMinX"]
        ordy = conversion["mapBoundsMaxY"] - (bus["y"] - 0.5) * conversion["mapConversionY"]
        print(ordy, ",", ordx)
