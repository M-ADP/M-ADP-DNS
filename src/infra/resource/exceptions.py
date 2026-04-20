class ResourceServerException(Exception):
    def __init__(self, message: str = "리소스 서버 오류가 발생했습니다.") -> None:
        super().__init__(message)
        self.message = message


class ResourceNotFoundException(ResourceServerException):
    def __init__(self) -> None:
        super().__init__("리소스 서버에서 리소스를 찾을 수 없습니다.")
