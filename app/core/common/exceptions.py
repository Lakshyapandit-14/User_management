from fastapi import HTTPException, status

# --- Custom Exception Classes ---

class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class UserAlreadyExistsException(HTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class InvalidCredentialsException(HTTPException):
    def __init__(self, detail: str = "Invalid username or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "You are not authorized to perform this action"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
#thes 2 new

class NotFoundException(Exception):
    def __init__(self, message: str = "Resource not found"):
        self.message = message
        super().__init__(self.message)



class AlreadyExistsException(Exception):
    def __init__(self, message: str = "Resource already exists"):
        self.message = message
        super().__init__(self.message)

# --- Optional Helper Function ---
def raise_http_exception(status_code: int, message: str):
    """Generic HTTP exception raiser"""
    raise HTTPException(status_code=status_code, detail=message)
