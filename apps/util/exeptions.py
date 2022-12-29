class HttpException(Exception):
    def __init__(self):
        self.is_custom = True
        self.message  = ''
        self.status   = None

    def __str__(self):
        return self.message

class BadRequestException(HttpException):
    def __init__(self, message):
        super().__init__()
        self.message = message
        self.status  = 400

class UnauthorizedException(HttpException):
    def __init__(self, message = 'Unauthorization'):
        super().__init__()
        self.message = message
        self.status  = 401

class ForbiddenException(HttpException):
    def __init__(self, message =  "Don't have permission"):
        super().__init__()
        self.message = message
        self.status  = 403
        
class NotFoundException(HttpException):
    def __init__(self, message = 'Not found url'):
        super().__init__()
        self.message = message
        self.status  = 404
        