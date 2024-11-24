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


class InvalidScanSchema(HTTPException):
    def __init__(
        self,
        message: str = "Некорректный запрос",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)


class InvalidVersionIntensity(HTTPException):
    def __init__(
        self,
        message: str = "Некорректное значение интенсивности сканирования",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)


class InvalidSpecificRange(HTTPException):
    def __init__(
        self,
        message: str = "Некорректный диапазон портов",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)


class InvalidTopPortRange(HTTPException):
    def __init__(
        self,
        message: str = "Некорректное количество портов",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)


class InvalidRate(HTTPException):
    def __init__(
        self,
        message: str = "Некорректное значение скорости сканирования",
        status_code: int = 400,
    ) -> None:
        super().__init__(status_code, detail=message)
