from datetime import datetime
from app.repository import OrderRepository
from app.schemas import OrderCreate, OrderUpdate, OrderStatus, Order
from app.exceptions import OrderNotFoundError, OrderAlreadyCompletedError


class OrderService:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    def create_order(self, order_in: OrderCreate) -> Order:
        new_order = Order(
            id=self.repo.get_next_id(),
            **order_in.model_dump(),
            status=OrderStatus.pending,
            created_at=datetime.now()
        )
        return self.repo.add(new_order)

    def list_orders(self, status_filter: OrderStatus | None = None) -> list[Order]:
        orders = self.repo.get_all()
        if status_filter:
            orders = [o for o in orders if o.status == status_filter]
        return orders

    def get_order(self, order_id: int) -> Order:
        order = self.repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(order_id)
        return order

    def update_order(self, order_id: int, order_update: OrderUpdate) -> Order:
        order = self.get_order(order_id)

        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)

        update_data = order_update.model_dump(exclude_unset=True)
        return self.repo.update(order_id, update_data)

    def delete_order(self, order_id: int) -> None:
        order = self.get_order(order_id)

        if order.status == OrderStatus.completed:
            raise OrderAlreadyCompletedError(order_id)

        self.repo.delete(order_id)