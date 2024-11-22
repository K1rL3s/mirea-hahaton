from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseAlchemyModel


class ScanResult(BaseAlchemyModel):
    __tablename__ = "scan_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ip_address: Mapped[str] = Column(String, nullable=False)
    ptr_record: Mapped[str] = Column(String)
    severity: Mapped[str] = Column(String)  # Критичность уязвимостей

    ports: Mapped[int] = relationship("OpenPort", back_populates="scan_result")
