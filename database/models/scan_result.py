from uuid import UUID as UUID4

from sqlalchemy import UUID, Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import BaseAlchemyModel


# TODO: попробовать as_uuid=False и селект не с uuid'ом
class ScanResult(BaseAlchemyModel):
    __tablename__ = "scan_results"

    id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True)
    ip: Mapped[str] = Column(String(16), nullable=False, primary_key=True)
    ptr_record: Mapped[str] = Column(String(1024))
    severity: Mapped[str] = Column(String(1024))  # Критичность уязвимостей

    open_ports: Mapped[int] = relationship("OpenPort", back_populates="scan_result")
