import re
from repositories.customer_repository import CustomerRepository
from models.customer import Customer

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]{1,30}@[A-Za-z0-9.-]{1,30}+\.[A-Za-z]{2,15}$")

class CustomerService:
    def __init__(self, repository : CustomerRepository):
        self._repostory = repository

    def validate_email_format(self, email : str) -> bool:
        return re.fullmatch(EMAIL_PATTERN, email) is not None
