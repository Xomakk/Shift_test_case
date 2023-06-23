import uuid
from datetime import datetime, timedelta
from sqlalchemy import Integer, Column, ForeignKey, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP
from src.database import Base


class Salary(Base):
    __tablename__ = "salary"

    id = Column(UUID, index=True, primary_key=True, default=uuid.uuid4)
    size = Column(Integer, nullable=False)
    increase_date = Column(TIMESTAMP(timezone=True), default=lambda: datetime.utcnow() + timedelta(days=90))
    user_id = Column(UUID, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User")
