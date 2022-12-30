import json
import re

from apps.util.exeptions import BadRequestException

class PostUsersDto:
    def __init__(self, request_body):
        request_body = json.loads(request_body)
        self.email        = request_body['email']
        self.password     = request_body['password']

        self._validate_email()
        self._validate_password()

    def _validate_email(self):
        EMAIL_REGEX  = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        if not re.fullmatch(EMAIL_REGEX, self.email):
            raise BadRequestException('Invalid email')

    def _validate_password(self):
        PASSWORD_REGEX = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'

        if not re.fullmatch(PASSWORD_REGEX, self.password):
            raise BadRequestException(message = 'Invalid password')