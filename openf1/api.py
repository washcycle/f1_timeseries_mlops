import datetime
import json
import time
from dataclasses import dataclass, fields, asdict
from typing import Optional

import requests
from requests.models import PreparedRequest


from influxdb_client import Point


@dataclass
class CarData:
    brake: int
    date: datetime.datetime
    driver_number: int
    drs: int
    meeting_key: str
    n_gear: int
    rpm: int
    session_key: str
    speed: float
    throttle: float

    def __post_init__(self):
        if isinstance(self.date, str):
            self.date = datetime.datetime.fromisoformat(self.date)

    def to_influxdb_point(self) -> Point:
        point = Point("car_data")
        point.tag("driver_number", self.driver_number)
        point.tag("session_key", self.session_key)
        point.tag("meeting_key", self.meeting_key)
        point.field("brake", self.brake)
        point.field("drs", self.drs)
        point.field("n_gear", self.n_gear)
        point.field("rpm", self.rpm)
        point.field("speed", self.speed)
        point.field("throttle", self.throttle)
        point.time(self.date)
        return point


@dataclass
class Driver:
    session_key: int
    meeting_key: int
    broadcast_name: str
    country_code: str
    first_name: str
    full_name: str
    headshot_url: str
    last_name: str
    driver_number: int
    team_colour: str
    team_name: str
    name_acronym: str


class OpenFAPIRequest:
    pass


class OpenF1APIResponse:
    pass


class OpenF1API:
    def __init__(self, base_url: str = "https://api.openf1.org/"):
        self.base_url = base_url if base_url.endswith("/") else f"{base_url}/"

    def get_car_data(self, driver_number: int, session_key: str) -> list[CarData]:
        url = f"{self.base_url}v1/car_data"
        params = {
            "driver_number": driver_number,
            "session_key": session_key,
        }
        req = PreparedRequest()
        req.prepare_url(url, params)
        response = requests.get(req.url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch car data: {response.status_code}")

        car_data_list = [CarData(**data) for data in response.json()]
        return car_data_list

    def get_drivers(self, session_key: int, driver_number: int = None) -> list[Driver]:
        url = f"{self.base_url}v1/drivers"
        params = {
            "driver_number": driver_number,
            "session_key": session_key,
        }
        req = PreparedRequest()
        req.prepare_url(url, params)
        response = requests.get(req.url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch car data: {response.status_code}")

        drivers = [Driver(**data) for data in response.json()]
        return drivers

    def get_sessions(self):
        pass
