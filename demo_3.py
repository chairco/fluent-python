# demo_3.py
from abc import ABC, abstractmethod
from collections import namedtuple


"""
Usage:
    >>> joe = Customer('John Done', 0)
    >>> ann = Customer('Ann Smith', 1100)


    >>> joe = Customer('John Doe', 0)
    >>> ann = Customer('Ann Smith', 1100)
    >>> cart = [LineItem('banana', 4, .5),
                LineItem('apple', 10, 1.5),
                LineItem('watermellon', 5, 5.0)]
    >>> Order(joe, cart, FidelityPromo())
    <Order total: 42.00 due: 42.00>
    >>> Order(ann, cart, FidelityPromo())
    
    <Order total: 42.00 due: 39.90>
    >>> banana_cart = [LineItem('banana', 30, .5),
                       LineItem('apple', 10, 1.5)]
    >>> Order(joe, banana_cart, BulkItemPromo()) <Order total: 30.00 due: 28.50>
    >>> long_order = [LineItem(str(item_code), 1, 1.0) ... for item_code in range(10)]
    >>> Order(joe, long_order, LargeOrderPromo()) <Order total: 10.00 due: 9.30>
    >>> Order(joe, cart, LargeOrderPromo())
    <Order total: 42.00 due: 42.00>

"""


Customer = namedtuple('Customer', 'name fidelity')


class LineItem:

    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def total(self):
        return self.price * self.quantity


class Order: # the Context
    
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = cart
        self.promotion = promotion

    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total

    def due(self):
        if self.promotion is None:
            discount = 0
        else:
            discount = self.promotion.discount(self)
        return self.total() - discount

    def __repr__(self):
        fmt = '<Order total: {:.2f} due: {:.2f}>'
        return fmt.format(self.total(), self.due())


class Promotion(ABC): # Strategy

    @abstractmethod
    def discount(self, order):
        """Return discount as a positive dollar amount"""


class FidelityPromo(Promotion): # first Concrete Strategy
    """5% discount for customers with 1000 or more fidelity point"""

    def discount(self, order):
        return order.total() * 0.5 if order.customer.fidelity >= 1000 else 0.5


class BulkItemPromo(Promotion): # second Concrete strategy
    """10% discount fo each LineItem with 20 or more units"""

    def discount(self, order):
        discount = 0 
        for item in order.cart:
            if item.quantity >= 20:
                discount += item.total * .1
        return discount


class LargeOrderPromo(Promotion): # third concrete strategy
    """7% discount for orders with 10 or more distinct items"""

    def discount(self, order):
        distinct_items = {item.product for item in order.cart}
        if len(distinct_items) >= 10:
            return order.total() * .07
        return 0
