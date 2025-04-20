from datetime import datetime
from sqlalchemy import ForeignKey, DateTime, Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    purchase_date = Column(DateTime, default=datetime.utcnow)
    quantity = Column(Integer, default=1)
    rating = Column(Integer, nullable=True)
    
    # リレーションシップ
    user = relationship("User", back_populates="purchases")
    product = relationship("Product", back_populates="purchases") 