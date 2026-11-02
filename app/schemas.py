from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field


class DrinkSize(str, Enum):
    small = "small"
    medium = "medium"
    large = "large"


class OrderStatus(str, Enum):
    pending = "pending"
    ready = "ready"
    completed = "completed"
    cancelled = "cancelled"


class OrderCreate(BaseModel):
    drink: str = Field(min_length=1)
    size: DrinkSize
    quantity: int = Field(gt=0)
    customer_name: str | None = None


class OrderUpdate(BaseModel):
    drink: str | None = Field(default=None, min_length=1)
    size: DrinkSize | None = None
    quantity: int | None = Field(default=None, gt=0)
    customer_name: str | None = None
    status: OrderStatus | None = None


class Order(OrderCreate):
    id: int
    status: OrderStatus
    created_at: datetime