# -*- coding: utf-8 -*-
# web2py/applications/<your_application>/controllers
from cart import Cart
from cart import OrderError



def add():
    product = db(db.product.id == request.args(0)).select().first()
    cart = Cart()
    if product.id in cart:
        try:
            # product.qty should be an int that represents
            # the amount avaiable of the product.
            # If amount of the order > amount_avaiable, an exception
            # will be raised.
            # If amount_avaiable is not set, the module won't check
            # the avaiable.
            cart.AddAmount(product.id, amount_avaiable=product.qty)
        except OrderError as e:
            return e
    else:
        carrinho.NewOrder(produto.id)
    return locals()


def remove():
    product = db(db.product.id == request.args(0)).select().first()
    cart = Cart()
    try:
        # If the order is not found, an exception will be raised.
        cart.DecreaseAmount(product.id)
    except OrderError as e:
        return e
    return locals()


def show():
    cart = Cart()
    cart_dict = cart.ShowCart() # A dict with all orders.
    for id, amount in cart:
        # Do something or
        pass
    return locals()


