from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100))
    hashed_password = Column(String)

    # リレーションシップ
    purchases = relationship("Purchase", back_populates="user") 