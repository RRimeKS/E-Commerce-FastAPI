from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    firstName = Column(String(64))
    lastName = Column(String(64))
    userName = Column(String(64), unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password = Column(String(64))
    isActive = Column(Boolean, default=False)
    role = Column(String(32), default="user")

    orders = relationship("Order", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    createdAt = Column(DateTime(timezone=True), server_default=func.now())
    updatedAt = Column(DateTime(timezone=True), onupdate=func.now())