from pydantic import BaseModel
from typing import Sequence
from datetime import datetime

from app.db.models import Result


class ReportInfo(BaseModel):
    id: int
    position: int
    abbreviation: str
    driver: str
    team: str
    start: datetime
    end: datetime
    result: int


class DriverInfo(BaseModel):
    id: int
    abbreviation: str
    name: str
    team: str


def serialize_report(result: Sequence[Result]) -> list[ReportInfo]:
    return [
        ReportInfo(
            id=info.id,
            position=info.position,
            abbreviation=info.driver.abbreviation,
            driver=info.driver.name,
            team=info.driver.team.name,
            start=info.start,
            end=info.end,
            result=info.result,
        )
        for info in result
    ]


def serialize_drivers(result: Sequence[Result]) -> list[DriverInfo]:
    return [
        DriverInfo(
            id=info.id,
            abbreviation=info.driver.abbreviation,
            name=info.driver.name,
            team=info.driver.team.name,
        )
        for info in result
    ]
