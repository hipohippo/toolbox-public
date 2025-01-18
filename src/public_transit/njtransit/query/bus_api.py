"""
projecte parked due to anti-robot mechanism on njtransit.com
"""

import re
from typing import List

from bs4 import BeautifulSoup
from nodriver.core.browser import Browser
from public_transit.njtransit.query.bus_and_stop import BUS_NUMBERS, NextBus, NJTBusStop


def format_bus_message(
    stop: NJTBusStop, bus_arrivals: List[NextBus], direction: str
) -> str:
    message = (f"To <b>{direction}</b> StopID={stop.id}:\n") + (
        "\n".join([bus.to_html() for bus in bus_arrivals])
        if bus_arrivals
        else "No bus found"
    )
    return message


async def extract_content_from_page(
    stop: NJTBusStop, busno: str, browser: Browser
) -> BeautifulSoup:
    tab1 = await browser.get(
        f"https://mybusnow.njtransit.com/bustime/wireless/html/eta.jsp?route={busno}&id={stop.id}&showAllBusses=off"
    )
    await tab1.wait_for(selector="body")
    page_body = await tab1.query_selector("body")
    page_content = await page_body.get_html()
    return BeautifulSoup(page_content, features="lxml")


def parse_content_from_page(
    stop: NJTBusStop, page_content: BeautifulSoup
) -> List[NextBus]:
    scheduled_bus_and_arrivals = page_content.find_all(
        "strong", attrs={"class": "larger"}
    )
    capacity = page_content.find_all("span", attrs={"class": "smaller"})
    bus_and_prediction = [
        element.text.replace("\xa0", "") for element in scheduled_bus_and_arrivals
    ]
    vehicle_info = [re.sub("[\n\t\xa0]", "", cap.text) for cap in capacity]

    num_arrival_info = len(bus_and_prediction) // 2
    return [
        NextBus(
            stop,
            bus_and_prediction[2 * i],
            bus_and_prediction[2 * i + 1],
            vehicle_info[i],
        )
        for i in range(num_arrival_info)
    ]


async def next_bus_job(stop: NJTBusStop, direction: str, browser: Browser) -> str:
    bus_arrivals = []
    for busno in BUS_NUMBERS:
        page_content: BeautifulSoup = await extract_content_from_page(
            stop, busno, browser
        )
        bus_arrivals.extend(parse_content_from_page(stop, page_content))

    bus_arrivals.sort(key=lambda x: x.departure_time)
    message = format_bus_message(stop, bus_arrivals, direction)
    return message
