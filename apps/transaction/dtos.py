import json
import re

from apps.util.exeptions import BadRequestException

class PostTransactionsDto:
    def __init__(self, request_body):
        request_body = json.loads(request_body)

        self.deposit          = request_body['deposit']
        self.title            = request_body.get('title','')
        self.description      = request_body.get('description','') 

        self._validate_description()
        self._validate_title()
        self._validate_deposit()

    def _validate_title(self):
        TITLE_REGEX = '^.{,20}$'
        
        if not re.fullmatch(TITLE_REGEX, self.title):
            raise BadRequestException('Invalid title')

    def _validate_description(self):
        DESCRIPTION_REGEX = '^.{,100}$'
        
        if not re.fullmatch(DESCRIPTION_REGEX, self.description):
            raise BadRequestException('Invalid description')

    def _validate_deposit(self):
        DEPOSIT_REGEX = '^[-]*[\d]+$'

        if not re.fullmatch(DEPOSIT_REGEX, self.deposit):
            raise BadRequestException('Invalid deposit')