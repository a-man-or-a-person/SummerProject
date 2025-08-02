from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from test_db.database import Base


class LinkStorage(Base):
    __tablename__ = 'links'

    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    long_link: Mapped[str]
    created_at = Column(
        DateTime,
        server_default=func.now(),  # Use func.current_timestamp() for some databases
        nullable=False
    )