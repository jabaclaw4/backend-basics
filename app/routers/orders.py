from fastapi import APIRouter, status, Response, Query
from app.schemas import Order, OrderCreate, OrderUpdate, OrderStatus
from app.dependencies import ServiceDep

router = APIRouter(prefix="/orders", tags=["Заказы"])


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Создать заказ")
def create_order(order_in: OrderCreate, service: ServiceDep):
    return service.create_order(order_in)


@router.get("/", response_model=list[Order], summary="Список заказов")
def list_orders(
    status_filter: OrderStatus | None = Query(None, alias="status"),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    service: ServiceDep = None
):
    orders = service.list_orders(status_filter)
    return orders[offset : offset + limit]


@router.get("/{order_id}", response_model=Order, summary="Получить заказ")
def get_order(order_id: int, service: ServiceDep):
    return service.get_order(order_id)


@router.patch("/{order_id}", response_model=Order, summary="Обновить заказ")
def update_order(order_id: int, order_update: OrderUpdate, service: ServiceDep):
    return service.update_order(order_id, order_update)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Отменить заказ")
def delete_order(order_id: int, service: ServiceDep):
    service.delete_order(order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)