class ResourceServerException(Exception):
    def __init__(self, message: str = "리소스 서버 오류가 발생했습니다.") -> None:
        super().__init__(message)
        self.message = message
