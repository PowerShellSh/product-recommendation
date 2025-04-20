from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Decimal = Field(..., ge=0)
    category: str = Field(..., min_length=1, max_length=100)
    image_url: Optional[str] = Field(None, max_length=500)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    price: Optional[Decimal] = Field(None, ge=0)
    category: Optional[str] = Field(None, min_length=1, max_length=100)

class Product(ProductBase):
    id: int
    
    class Config:
        from_attributes = True 