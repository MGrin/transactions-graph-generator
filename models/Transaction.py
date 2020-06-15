from mimesis import Datetime, Business
import random
from math import ceil
from uuid import uuid4
from .Node import Node


class Transaction(Node):
    _datetime = Datetime()
    _business = Business()

    def __init__(self, sourceId: int, targetId: int):
        self.__type = "Transaction"
        self.id = uuid4()
        self.source = sourceId
        self.target = targetId
        self.date = self._datetime.date(start=2000, end=2020)
        self.time = self._datetime.time()

        self.amount = random.randint(1, 10000)
        if random.random() < 0.15:
            self.currency = self._business.currency_iso_code()
        else:
            self.currency = None

