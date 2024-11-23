from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base import BaseAlchemyModel


class VulnerabilityModel(BaseAlchemyModel):
    __tablename__ = "vulnerabilities"

    id: Mapped[str] = mapped_column(String(1024), primary_key=True)
    name: Mapped[str] = mapped_column(String(1024), nullable=False)
    description: Mapped[str] = mapped_column(String(1024), nullable=False)
    vendor: Mapped[str] = mapped_column(String(1024), nullable=False)
    soft_name: Mapped[str] = mapped_column(String(1024), nullable=False)
    version: Mapped[str] = mapped_column(String(1024), nullable=False)
    type: Mapped[str] = mapped_column(String(1024), nullable=False)
    os: Mapped[str] = mapped_column(String(1024), nullable=False)
    class_: Mapped[str] = mapped_column(String(1024), nullable=False)
    date: Mapped[str] = mapped_column(String(1024), nullable=False)
    cvss2: Mapped[str] = mapped_column(String(1024), nullable=False)
    cvss3: Mapped[str] = mapped_column(String(1024), nullable=False)
    danger_level: Mapped[str] = mapped_column(String(1024), nullable=False)
    elimination_methods: Mapped[str] = mapped_column(String(1024), nullable=False)
    status: Mapped[str] = mapped_column(String(1024), nullable=False)
    is_exploitation: Mapped[str] = mapped_column(String(1024), nullable=False)
    elimination_info: Mapped[str] = mapped_column(String(1024), nullable=False)
    urls: Mapped[str] = mapped_column(String(1024), nullable=False)
    other_id: Mapped[str] = mapped_column(String(1024), nullable=False)
    other_info: Mapped[str] = mapped_column(String(1024), nullable=False)
    realtions: Mapped[str] = mapped_column(String(1024), nullable=False)
    method_exploitation: Mapped[str] = mapped_column(String(1024), nullable=False)
    method_fix: Mapped[str] = mapped_column(String(1024), nullable=False)
    cwe_description: Mapped[str] = mapped_column(String(1024), nullable=False)
    cwe_type: Mapped[str] = mapped_column(String(1024), nullable=False)
