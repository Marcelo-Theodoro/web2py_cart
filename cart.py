# -*- coding: utf-8 -*-
from gluon import current


class OrderError(Exception):
    pass

class Cart(Object):
    '''
    A web2py module to store orders in the session.
    The orders are stored in the session.cart as a dict.
    With the key=product.id, and value=(product.id, amount of products)
    More infos: https://github.com/Marcelo-Theodoro/web2py_cart
    '''

    def __init__(self):
        if not current.session.cart:
            current.session.cart = {}
        self.cart = current.session.cart
        self._components = [self.cart[n] for n in self.cart]
        self._products = [self.cart[n][0] for n in self.cart]

    def __repr__(self):
        return ', '.join([str(self.cart[n]) for n in self.cart])

    def __iter__(self):
        return iter(self._components)

    def __getitem__(self, index):
        return self._components[index]

    def __len__(self):
        return len(self._components)

    def __contains__(self, product):
        return product in self._products

    def NewOrder(self, product):
        '''
        Add a new order in the cart.
        '''
        if self.__contains__(product):
            raise OrderError('Order Already Exists')
        self.cart[product] = (product, 1)

    def AddAmount(self, product, amount_requested=1, amount_avaiable=False):
        '''
        Add +amount_requested in the amount at product order.
        amount_requested default is 1.
        amount_avaiable should be an int of how many product are avaiable or False,
        if False, AddAmount() won't check if the amount_requested is avaiable.
        '''
        if amount_avaiable and not self.AmountAvailable(product, amount_requested,
                                                        amount_avaiable):
            raise OrderError('Amount Not Avaiable')
        try:
            self.cart[product] = (self.cart[product][0],
                                  self.cart[product][1] + amount_requested)
        except KeyError:
            raise OrderError('Order Does Not Exists')

    def RemoveOrder(self, product):
        '''
        Delete the order of the given product.
        '''
        try:
            self.cart.pop(product)
        except KeyError:
            raise OrderError('Order Does Not Exists')

    def DecreaseAmount(self, product, amount_decrease=1):
        '''
        Decrease -amount_decrease in the order of the product.
        If the amount = 0, the order is removed.
        '''
        try:
            if self.cart[product][1] - 1 > 0:
                self.cart[product] = (self.cart[product][0],
                                      self.cart[product][1] - amount_decrease)
            else:
                self.RemoveOrder(product)
        except KeyError:
            raise OrderError('Order Does Not Exists')

    def ShowCart(self):
        '''
        Return a list of dicts containing all the orders
        of the cart.
        '''
        orders_list = []
        for order in self.cart:
            product_id = self.cart[order][0]
            product_amount = self.cart[order][1]
            orders_list.append({'id': product_id, 'amount': product_amount})
        return orders_list

    def AmountProductOrder(self, product):
        '''
        Return the amount of the product order.
        None if the order is not found.
        '''
        return ''.join(str(n[1]) for n in self._components if n[0] == product) or None

    def AmountAvailable(self, product, amount_requested, amount_available):
        '''
        Return True if the amount of the product is available,
        else False.
        '''
        if self.__contains__(product):
            return amount_requested + int(self.AmountProductOrder(product)) <= amount_available
        return amount <= self.AMOUNT_AVAILABLE


