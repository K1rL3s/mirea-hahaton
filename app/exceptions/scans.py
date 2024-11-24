from fastapi import HTTPException


class InvalidIP(HTTPException):
    def __init__(
        self,
        message: str = "Некорректный IP адрес",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)


class InvalidIPRange(InvalidIP):
    def __init__(
        self,
        message: str = "Некорректный или слишком большой диапазон IP адресов",
        status_code: int = 400,
    ) -> None:
        super().__init__(message=message, status_code=status_code)


class InvalidIPCIDR(InvalidIP):
    def __init__(
        self,
        message: str = "Некорректный или слишком большой диапазон IP адресов",
        status_code: int = 400,
    ) -> None:
        super().__init__(message=message, status_code=status_code)
