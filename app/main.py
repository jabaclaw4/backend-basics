from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import orders
from app.exceptions import OrderNotFoundError, OrderAlreadyCompletedError
from app.dependencies import SettingsDep

app = FastAPI(
    title="Coffee Orders API",
    description="Сервис учёта заказов (слои)",
    version="1.0.0"
)


@app.exception_handler(OrderNotFoundError)
def handle_not_found(request: Request, exc: OrderNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)}
    )


@app.exception_handler(OrderAlreadyCompletedError)
def handle_completed(request: Request, exc: OrderAlreadyCompletedError):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)}
    )


app.include_router(orders.router)


@app.get("/", tags=["Сервис"], summary="Приветствие")
def read_root():
    return {"message": "Добро пожаловать!"}


@app.get("/info", tags=["Сервис"], summary="Информация")
def get_info(settings: SettingsDep):
    return {"app_name": settings.app_name}