import uuid
import datetime

from sqlalchemy import String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID


class Base(DeclarativeBase):
    pass;

class Application(Base):
    __tablename__ = "application"
    application_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    student_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    program_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    served_staff_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    status: Mapped[str] = mapped_column(String(50))
    submission_date: Mapped[datetime.date] = mapped_column(Date())

