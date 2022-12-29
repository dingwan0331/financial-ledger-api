import re

from .exeptions import BadRequestException

def validate_email(value):
    EMAIL_REGEX  = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.fullmatch(EMAIL_REGEX, value):
        raise BadRequestException('Invalid email')

def validate_password(value):
    PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

    if not re.fullmatch(PASSWORD_REGEX, value):
        raise BadRequestException(message = 'Invalid password')