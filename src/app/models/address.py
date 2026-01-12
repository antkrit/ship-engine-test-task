import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from uuid6 import uuid7

from ..core.db.database import Base


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True, init=False)

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(UUID(as_uuid=True), default_factory=uuid7, unique=True)

    name: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    company: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True, default=None)
    address_line1: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    address_line2: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    address_line3: Mapped[str | None] = mapped_column(String(200), nullable=True, default=None)
    city_locality: Mapped[str | None] = mapped_column(String(100), nullable=True, default=None)
    state_province: Mapped[str | None] = mapped_column(String(50), nullable=True, default=None)
    postal_code: Mapped[str | None] = mapped_column(String(20), nullable=True, default=None)
    country_code: Mapped[str | None] = mapped_column(String(2), nullable=True, default=None)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default_factory=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)

