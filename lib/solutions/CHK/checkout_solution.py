""" Diary
* 2024-09-07 Sun
** 0935

On starting this morning there was an alert:

  IMPORTANT! You are not allowed to work on the solution while the challenge is PAUSED.

This wasn't anywhere in the documentation.  I did ~60 mins last night, pencil & paper sketches and refactoring.

"""

# +------+-------+----------------+
# | Item | Price | Special offers |
# +------+-------+----------------+
# | A    | 50    | 3A for 130     |
# | B    | 30    | 2B for 45      |
# | C    | 20    |                |
# | D    | 15    |                |
# +------+-------+----------------+

PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    }
LEGAL_SKUS = PRICES.keys()

def multiple_price(basket, sku, context):
    multi_amount = context['amount']
    multi_price = context['price']
    while basket.to_pay_for.get(sku, 0) >= multi_amount:
        basket.to_pay_for[sku] -= multi_amount
        basket.paid_for.setdefault(sku, 0)
        basket.paid_for[sku] += multi_amount
        basket.price += multi_price
    return basket

DISCOUNTS = {
    'A': (multiple_price, {'amount': 3, 'price': 130}),
    'B': (multiple_price, {'amount': 2, 'price': 45}),
    }

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not valid(skus):
        return -1
    order = parse_skus(skus)
    basket = Basket(order)
    ds = applicable_discounts(basket)
    for d in ds:
        basket = apply_discount(d, basket)
    basket.apply_vanilla_prices()
    return basket.price

def valid(skus):
    return all([i in LEGAL_SKUS for i in skus])

def parse_skus(skus):
    d = {}
    for i in skus:
        if i in LEGAL_SKUS:
                d.setdefault(i, 0)
                d[i] += 1
    return d
    
def applicable_discounts(basket):
    return [(sku, config) for (sku,config) in DISCOUNTS.items()
            if sku in basket.to_pay_for.keys()
            ]

def apply_discount(discount, basket):
    sku, config = discount
    f, context = config
    return f(basket, sku, context)

class Basket:
    def __init__(self, order):
        self.price = 0
        self.paid_for = dict()
        self.to_pay_for = order

    def apply_vanilla_prices(self):
        for sku, amount in self.to_pay_for.items():
            self.price += PRICES[sku] * amount
            # self.to_pay_for.pop(sku) # TODO

