import logging

from sqlalchemy import text, create_engine
from sqlalchemy.exc import ProgrammingError

from app.utils.report.report import Report
from app.config import settings
from app.db.session import get_session
from app.db.models import Race, Driver, Result, Team


log = logging.getLogger(__name__)


def create_database(db_name: str) -> None:
    try:
        with create_engine(
            settings.DATABASE_URL, isolation_level='AUTOCOMMIT'
        ).begin() as conn:
            conn.execute(text(f'CREATE DATABASE {db_name};'))
    except ProgrammingError:
        log.error('Database %s already exists', db_name)
    else:
        log.info('Database %s created', db_name)


def drop_database(db_name: str) -> None:
    try:
        with create_engine(
            settings.DATABASE_URL, isolation_level='AUTOCOMMIT'
        ).begin() as conn:
            conn.execute(text(f'DROP DATABASE {db_name} WITH (FORCE);'))
    except ProgrammingError:
        log.error('Database %s does not exist', db_name)
    else:
        log.info('Database %s dropped', db_name)


def init_db(db_url: str) -> None:
    import alembic.config
    import alembic.command

    alembic_config = alembic.config.Config('alembic.ini')
    alembic_config.set_main_option('sqlalchemy.url', f'{db_url}')
    alembic.command.upgrade(alembic_config, 'head')
    log.info('Alembic upgrade db: %s', db_url)


def load_data_to_db(instance: Report) -> None:
    data = instance.sort_report()

    with get_session() as session:
        race_instance = Race(
            title='Monaco 2018',
            year=2018,
        )

        teams = {}
        for driver, info in data.items():
            team_name = info.get('Team')
            if driver not in teams:
                team_instance = Team(
                    name=team_name,
                )
                teams[driver] = team_instance

        drivers = {}
        for driver, info in data.items():
            if driver not in drivers:
                driver_instance = Driver(
                    name=info.get('Driver'),
                    abbreviation=info.get('Abbreviation'),
                    team=teams.get(driver),
                )
                drivers[driver] = driver_instance

        results = []
        for driver, info in data.items():
            if driver not in results:
                result = info.get('Result')
                assert result is not None

                result_instance = Result(
                    driver=drivers.get(driver),
                    race=race_instance,
                    start=info.get('Start'),
                    end=info.get('End'),
                    result=result * 1000,
                    position=info.get('Position'),
                )
                results.append(result_instance)
            session.add_all(results)

        session.commit()
