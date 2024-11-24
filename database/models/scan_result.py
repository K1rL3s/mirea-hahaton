import datetime
from uuid import UUID as UUID4

from sqlalchemy import UUID, Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseAlchemyModel


# TODO: попробовать as_uuid=False и селект не с uuid'ом
class ScanResultModel(BaseAlchemyModel):
    __tablename__ = "scan_results"

    id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True)
    ip: Mapped[str] = mapped_column(String(16), nullable=False, primary_key=True)
    end: Mapped[str] = mapped_column(Boolean, nullable=False, default=False)
    ptr_record: Mapped[str] = mapped_column(String(1024), nullable=True)
    severity: Mapped[str] = mapped_column(String(1024), nullable=True)

    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.datetime.utcnow,
        onupdate=datetime.datetime.utcnow,
        server_default=func.now(),
        server_onupdate=func.now(),
    )
