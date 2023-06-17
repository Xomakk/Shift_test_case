from datetime import datetime, timedelta
from sqlalchemy import Integer, TIMESTAMP, Column, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base


class Salary(Base):
    __tablename__ = "salary"

    id = Column(Integer, index=True, primary_key=True)
    size = Column(Integer, nullable=False)
    increase_date = Column(TIMESTAMP, default=lambda: datetime.utcnow() + timedelta(days=90))
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))

    user = relationship("User")
