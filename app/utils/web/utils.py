from typing import Sequence, Optional, Any

from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from app.db.models import Result, Driver
from app.db.session import get_session


def get_results(abbr: Optional[str] = None) -> Sequence[Result]:
    query = select(Result).options(
        selectinload(Result.driver).joinedload(Driver.team),
        joinedload(Result.race),
    )

    if abbr is not None:
        query = query.where(Result.driver.and_(Driver.abbreviation == abbr))

    with get_session() as session:
        return session.scalars(query).all()


def desc_result(result) -> list[Any]:
    return sorted(result, key=lambda x: x.position, reverse=True)
