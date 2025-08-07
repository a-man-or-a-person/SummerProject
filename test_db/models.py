from DB.database import Base
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class LinkStorage(Base):
    __tablename__ = "links"

    short_link_id: Mapped[str] = mapped_column(
        primary_key=True, unique=True, autoincrement=False
    )
    long_link: Mapped[str]
    created_at = Column(
        DateTime,
        server_default=func.now(),  # Use func.current_timestamp() for some databases
        nullable=False,
    )
