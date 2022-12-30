import json
import re

from apps.util.exeptions import BadRequestException
from django.db.models    import Q

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

class PatchTransactionDto:
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

class GetTransactionsDto:
    _filter_set = {
        'income'      : Q(deposit__gt = 0),
        'expenditure' : Q(deposit__lt = 0),
        'all'         : Q()
    }
    
    def __init__(self, request_query, user_id):
        self.order             = request_query.get('order', '-created_at')
        self._transaction_type = request_query.get('transaction-type', 'all')
        self.offset            = request_query.get('offset', '0')
        self.limit             = request_query.get('limit', '30')
        self.filter            = Q(user_id = user_id)

        self._validate_order()
        self._validate_is_income()
        self._set_offset()
        self._set_limit()
        self._set_filter()

    def _validate_order(self):
        _ORDER_LIST = ['-created_at', 'created_at']

        if self.order not in _ORDER_LIST:
            raise BadRequestException('Invalid order')

    def _validate_is_income(self):
        _TRANSACTION_TYPE_LIST = ['income', 'expenditure', 'all']

        if self._transaction_type not in _TRANSACTION_TYPE_LIST:
            raise BadRequestException('Invalid transaction type')

    def _set_filter(self):
        self.filter &= self._filter_set[self._transaction_type]

    def _set_offset(self):
        OFFSEET_REGEX = '\d+'
        if not re.fullmatch(OFFSEET_REGEX, self.offset):
            raise BadRequestException('Invalid offset')
        
        self.offset = int(self.offset)
    
    def _set_limit(self):
        LIMIT_REGEX = '\d+'

        if not re.fullmatch(LIMIT_REGEX, self.limit):
            raise BadRequestException('Invalid limit')

        self.limit = int(self.limit)