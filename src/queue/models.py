import datetime
import uuid

from sqlalchemy import TIMESTAMP, UUID
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass;

class Queue(Base):
    __tablename__ = "queue"

    queue_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    timestamp: Mapped[datetime.time] = mapped_column(TIMESTAMP)