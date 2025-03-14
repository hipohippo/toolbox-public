import json

import pandas as pd
import requests

from nationalpark.lodge_short_name import NationalPark, SHORT_NAME


def scrape_national_park_vacancy(
    national_park: NationalPark, dt: pd.Timestamp, nights: int
):
    lodge_raw = requests.get(
        rf"https://webapi.xanterra.net/v1/api/availability/hotels/{national_park.value}?"
        rf"date={dt.month}%2F{dt.day}%2F{dt.year}&limit=1&is_group=false&nights={nights}"
    )

    lodge = json.loads(lodge_raw.text)
    availability = lodge["availability"][dt.strftime("%m/%d/%Y")]
    short_names = SHORT_NAME[national_park]

    vacancy = {}
    for short_name, full_name in short_names.items():
        if short_name in availability:
            min_price = availability[short_name]["min"]
            if min_price > 0:
                vacancy[full_name] = min_price
    return vacancy


if __name__ == "__main__":
    scrape_national_park_vacancy(
        NationalPark.GRAND_CANYON, pd.Timestamp("2024-08-14"), 1
    )
