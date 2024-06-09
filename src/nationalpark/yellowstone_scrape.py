import json

import pandas as pd
import requests

dt = pd.Timestamp("2024-08-14")
nights = 1
national_park_webid = ["glaciernationalparklodges", "yellowstonenationalparklodges", "zionlodge"]  # and many more

glacier_short_name = {"GLCC": "", "GLLM": "", "GLMG": "", "GLRS": "", "GLSC": "", "GLVI": "Village Inn at Apgar"}

# aiohttp.request("GET")
yellowstone_lodge_short_name = {
    "YLCL": "CANYON LODGE",
    "YLGV": "GRANT VILLAGE",
    "YLMH": "MAMMOTH HOTEL",
    "YLLH": "LAKE HOTEL",
    "YLLL": "LAKE LODGE",
    "YLOI": "OLD FAITHFUL INN",
    "YLOL": "OLD FAITHFUL LODGE",
    "YLOS": "OLD FAITHFUL SNOW LODGE",
    "YLRL": "ROOSEVELT LODGE",
}


def scrape_national_park_vacancy(national_park_id: str):
    lodge_raw = requests.get(
        rf"https://webapi.xanterra.net/v1/api/availability/hotels/{national_park_id[0]}?"
        rf"date={dt.month}%2F{dt.day}%2F{dt.year}&limit=1&is_group=false&nights={nights}"
    )

    lodge = json.loads(lodge_raw.text)
    availability = lodge["availability"][dt.strftime("%m/%d/%Y")]
    print(availability.keys())
    for short_name, full_name in yellowstone_lodge_short_name.items():
        if availability[short_name]["min"] > 0:
            print(full_name, availability[short_name]["min"])
