from datetime import datetime
from enum import Enum
from functools import lru_cache

from fastapi import FastAPI, Depends, HTTPException, Query, status, Response
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Учёт заказов кофейни"
    default_page_size: int = 10
    max_page_size: int = 50

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings():
    return Settings()


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
    drink: str = Field(min_length=1, description="Название напитка из меню", examples=["Латте"])
    size: DrinkSize = Field(description="Размер напитка")
    quantity: int = Field(gt=0, description="Количество", examples=[1])
    customer_name: str | None = Field(default=None, description="Имя клиента", examples=["Ирина"])


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


app = FastAPI(
    title="Coffee Orders API",
    description="Сервис учёта заказов для бариста",
    version="1.0.0"
)

orders_db: dict[int, Order] = {}
next_id = 1


@app.get("/", tags=["Сервис"], summary="Приветствие")
def read_root():
    return {"message": "Добро пожаловать в сервис заказов!"}


@app.get("/info", tags=["Сервис"], summary="Информация о сервисе")
def get_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "orders_count": len(orders_db)
    }


@app.post(
    "/orders",
    response_model=Order,
    status_code=status.HTTP_201_CREATED,
    tags=["Заказы"],
    summary="Создать заказ"
)
def create_order(order_in: OrderCreate):
    global next_id
    new_order = Order(
        id=next_id,
        **order_in.model_dump(),
        status=OrderStatus.pending,
        created_at=datetime.now()
    )
    orders_db[next_id] = new_order
    next_id += 1
    return new_order


@app.get(
    "/orders",
    response_model=list[Order],
    tags=["Заказы"],
    summary="Список заказов"
)
def list_orders(
        status_filter: OrderStatus | None = Query(None, alias="status"),
        limit: int = Query(10, ge=1, le=50),
        offset: int = Query(0, ge=0)
):
    result = list(orders_db.values())
    if status_filter:
        result = [o for o in result if o.status == status_filter]

    return result[offset: offset + limit]


@app.get(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Получить заказ по ID"
)
def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return orders_db[order_id]


@app.patch(
    "/orders/{order_id}",
    response_model=Order,
    tags=["Заказы"],
    summary="Обновить заказ"
)
def update_order(order_id: int, order_update: OrderUpdate):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    stored_order = orders_db[order_id]
    update_data = order_update.model_dump(exclude_unset=True)
    updated_order = stored_order.model_copy(update=update_data)
    orders_db[order_id] = updated_order

    return updated_order


@app.delete(
    "/orders/{order_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Заказы"],
    summary="Отменить заказ"
)
def delete_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    del orders_db[order_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)