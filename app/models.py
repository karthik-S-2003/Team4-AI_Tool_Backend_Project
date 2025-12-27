from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class AITool(Base):
    __tablename__ = "tools"
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    use_case = Column(String)
    category = Column(String)
    pricing_type = Column(String)
    average_rating = Column(Float, default=0.0)
    reviews = relationship("Review", back_populates="tool", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True, index=True)
    tool_id = Column(String, ForeignKey("tools.id", ondelete="CASCADE"))
    rating = Column(Integer)
    comment = Column(String, nullable=True)
    status = Column(String, default="Pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    tool = relationship("AITool", back_populates="reviews")

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True, index=True)
    hashed_password = Column(String, nullable=False)
