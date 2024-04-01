from sqlalchemy import String, SmallInteger, ForeignKey, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from datetime import datetime
from typing_extensions import Annotated

from app.db.models.base import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
date = Annotated[datetime, mapped_column(DateTime)]
int_field = Annotated[int, mapped_column(Integer)]


class Driver(Base):
    __tablename__ = 'drivers'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(length=50))
    abbreviation: Mapped[str] = mapped_column(String(length=4), unique=True)
    team_id: Mapped[int] = mapped_column(
        ForeignKey('teams.id', ondelete='CASCADE')
    )
    team: Mapped['Team'] = relationship()


class Result(Base):
    __tablename__ = 'results'

    id: Mapped[intpk]
    race: Mapped['Race'] = relationship()
    race_id: Mapped[int] = mapped_column(
        ForeignKey('races.id', ondelete='CASCADE')
    )
    driver: Mapped['Driver'] = relationship()
    driver_id: Mapped[int] = mapped_column(
        ForeignKey('drivers.id', ondelete='CASCADE')
    )
    start: Mapped[date]
    end: Mapped[date]
    result: Mapped[int_field]
    stage: Mapped[str] = mapped_column(String(length=5), default='Q3')
    position: Mapped[int] = mapped_column(SmallInteger)


class Race(Base):
    __tablename__ = 'races'

    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(String(length=50))
    year: Mapped[int_field]


class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(length=50))
