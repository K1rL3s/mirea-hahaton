from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseAlchemyModel

if TYPE_CHECKING:
    from .scan_result import ScanResult


class OpenPort(BaseAlchemyModel):
    __tablename__ = "open_ports"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    port: Mapped[int] = mapped_column(Integer, nullable=False)
    protocol: Mapped[str] = mapped_column(String, nullable=False)
    service: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String)

    scan_result_id: Mapped[int] = mapped_column(Integer, ForeignKey("scan_results.id"))
    scan_result: Mapped["ScanResult"] = relationship(
        "ScanResult",
        back_populates="ports",
    )
