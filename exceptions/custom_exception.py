import sqlite3

class DataExistsException(sqlite3.IntegrityError):
    pass

class DataNotFoundException(Exception):
    pass

class DataNotFoundException(Exception):
    def __init__(self, status_code: int = 404, message: str = "Data not found"):
        self.status = False
        self.status_code = status_code
        self.message = message
        super().__init__(self.status_code, self.message)

class CustomException(Exception):
    def __init__(self, status_code: int = 404, message: str = "Data not found"):
        self.status = False
        self.status_code = status_code
        self.message = message
        super().__init__(self.status_code, self.message)