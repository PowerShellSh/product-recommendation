from decimal import Decimal
from sqlalchemy import String, Numeric, Column, Integer
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Numeric(10, 2))
    category = Column(String(100))
    image_url = Column(String(500))

    # リレーションシップ
    purchases = relationship("Purchase", back_populates="product") 