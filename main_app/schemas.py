from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


# --- USER SCHEMAS ---
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Only used when creating a user

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# --- ORDER ITEM SCHEMAS ---
class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    price_at_time_of_purchase: float

    class Config:
        from_attributes = True


# --- ORDER SCHEMAS ---
class OrderBase(BaseModel):
    status: str = "pending"

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    user_id: int
    total_price: float
    created_at: datetime
    items: List[OrderItem] = []

    class Config:
        from_attributes = True