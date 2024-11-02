import re
from enum import Enum
import pandas as pd
import logging
BUS_NUMBERS = ["156R", "159R", "158"]


class NJTBusStop(Enum):
    def __init__(self, stop_name: str, direction: str, id: int):
        self.stop_name: str = stop_name
        self.direction: str = direction
        self.id: int = id

    def __str__(self):
        return f"{self.name}, {self.id}"

    LHNY = "LH", "NY", 21831  ## lincoln harbor toward new york
    LHNJ = "LH", "NJ", 21830  ## lincoln harbor toward new jersey

    RWNY = "RW", "NY", 21923  ## Port Imperial at Riverwalk Place
    RWNJ = "RW", "NJ", 21921  ## Port Imperial at Riverwalk Place

    PABT = "PABT", "NJ", 26229  ## port authority bus terminal toward new jersey


class NextBus:
    def __init__(self, stop_id: NJTBusStop, bus_number: str, predicted_departure_str: str, vehicle_info: str):
        """
        :param stop:
        :param predicted_time:  must match the regex {[\d]+ MIN"
        :param bus_number:      <rn>
        """
        self.stop_id = stop_id
        self.bus_number = bus_number
        predicted_departure = re.match(r"[^\d]*([\d]+)[ ]*MIN", predicted_departure_str)
        if predicted_departure:
            self.predicted_departure_min = int(predicted_departure.group(1))
            self.predicted_departure_str = str(predicted_departure_str)
            self.departure_time = pd.Timestamp.now() + pd.Timedelta(f"{self.predicted_departure_min} min")
            self.departure_time_str = self.departure_time.strftime("%I:%M %p")
        else:
            self.predicted_departure_min = None
            self.predicted_departure_str = "DELAYED"
            self.departure_time = None
            self.departure_time_str = ""

        grps = re.search(r".*(\(Passengers: \w\)).+", vehicle_info)
        if grps:
            self.passengers_info = grps.group(1)
        else:
            self.passengers_info = ""

        if self.stop_id == NJTBusStop.PABT and self.departure_time:
            if self.departure_time.time() > pd.Timestamp("2024-01-01 22:00:00").time():
                self.gate = " Gate 301"
            else:
                self.gate = {"158": " Gate 202", "159R": "Gate 201-2", "156R": "Gate 201-3"}[self.bus_number]
        else:
            self.gate = ""

    def to_html(self) -> str:
        logging.info(
            f"{self.bus_number}{self.gate}: in <b>{self.predicted_departure_str}</b> @ <b>{self.departure_time_str} "
        )
        return (
            f"{self.bus_number}{self.gate}: in <b>{self.predicted_departure_str}</b> @ <b>{self.departure_time_str} "
            f"{self.passengers_info}</b>"
        )
