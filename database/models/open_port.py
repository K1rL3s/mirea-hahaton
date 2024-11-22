from typing import TYPE_CHECKING
from uuid import UUID as UUID4

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseAlchemyModel

if TYPE_CHECKING:
    from .scan_result import ScanResult


# TODO: попробовать as_uuid=False и селект не с uuid'ом
class OpenPort(BaseAlchemyModel):
    __tablename__ = "open_ports"

    id: Mapped[UUID4] = mapped_column(ForeignKey("scan_results.id"), primary_key=True)
    port: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)

    protocol: Mapped[str] = mapped_column(String, nullable=False)
    service: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String)

    scan_result: Mapped["ScanResult"] = relationship(
        "ScanResult",
        back_populates="ports",
    )
