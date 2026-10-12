class AppError(Exception):
    pass
class NotFoundError(AppError):
    pass
class ServiceUnavailableError(AppError):
    pass