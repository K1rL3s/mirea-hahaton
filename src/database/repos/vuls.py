from typing import Any

from sqlalchemy import select

from database.models import VulnerabilityModel
from database.repos.base import BaseAlchemyRepo


class VulsRepo(BaseAlchemyRepo):
    async def get_by_ilike(self, **kwargs: Any) -> list[VulnerabilityModel]:
        query = select(VulnerabilityModel).where(
            *(
                getattr(VulnerabilityModel, key).ilike(value)
                for key, value in kwargs.items()
            ),
        )
        result = await self.session.scalars(query)
        return list(result)
