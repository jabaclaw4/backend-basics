from schemas import Order


class OrderRepository:
    def __init__(self):
        self._orders: dict[int, Order] = {}
        self._next_id = 1

    def get_all(self) -> list[Order]:
        return list(self._orders.values())

    def get_by_id(self, order_id: int) -> Order | None:
        return self._orders.get(order_id)

    def add(self, order: Order) -> Order:
        self._orders[order.id] = order
        return order

    def update(self, order_id: int, update_data: dict) -> Order:
        order = self._orders[order_id]
        updated_order = order.model_copy(update=update_data)
        self._orders[order_id] = updated_order
        return updated_order

    def delete(self, order_id: int) -> None:
        del self._orders[order_id]

    def get_next_id(self) -> int:
        current_id = self._next_id
        self._next_id += 1
        return current_id