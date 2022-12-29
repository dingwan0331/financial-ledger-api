from django.db.models       import Manager
from django.db.utils        import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from ..util.exeptions import BadRequestException


class UserManager(Manager):
    def create(self, email, password):
        try:
            user = super().create(email = email, password = password)
            return user 

        except IntegrityError:
            raise BadRequestException('Duplicated email')

    def get_by_email(self, email):
        try:
            return self.get(email = email)
        
        except ObjectDoesNotExist:
            raise BadRequestException('Sign up first')