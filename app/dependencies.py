from typing import Annotated
from fastapi import Depends
from app.config import get_settings, Settings
from repository import OrderRepository
from service import OrderService

_repository = OrderRepository()


def get_repository() -> OrderRepository:
    return _repository


def get_service(repo: OrderRepository = Depends(get_repository)) -> OrderService:
    return OrderService(repo)


ServiceDep = Annotated[OrderService, Depends(get_service)]
SettingsDep = Annotated[Settings, Depends(get_settings)]