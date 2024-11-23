from uuid import UUID as UUID4

from sqlalchemy import Integer, String, UUID
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseAlchemyModel



# TODO: попробовать as_uuid=False и селект не с uuid'ом
class OpenPort(BaseAlchemyModel):
    __tablename__ = "open_ports"

    id: Mapped[UUID4] = mapped_column(UUID(as_uuid=True), primary_key=True)
    ip: Mapped[str] = mapped_column(String(16), primary_key=True)
    port: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String(36))
    protocol: Mapped[str] = mapped_column(String(36))
    service: Mapped[str] = mapped_column(String(256))
    version: Mapped[str] = mapped_column(String(128))
