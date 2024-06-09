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
    'A': [(multiple_price, {'amount': 3, 'price': 130}),
          (multiple_price, {'amount': 5, 'price': 200}),
          ],
    'B': [(multiple_price, {'amount': 2, 'price': 45})],
    }

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not valid(skus):
        return -1
    order = parse_skus(skus)
    basket = Basket(order)
    ds = applicable_discounts(basket)
    for dset in ds:
        print(dset)
        basket = apply_discounts(dset, basket)
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
    return [(sku, configs) for (sku,configs) in DISCOUNTS.items()
            if sku in basket.to_pay_for.keys()
            ]

def apply_discounts(discount_set, basket):
    sku, configs = discount_set
    if len(configs) == 1:
        config = configs[0]
        basket = apply_discount(basket, sku, config)
    else:
        # order discounts by ... some effect size criterion
        configs = sorted(configs,
                         key=lambda cfg: cfg[1].get('amount', 0),
                         reverse=True)
        # apply discounts in order
        for config in configs:
            basket = apply_discount(basket, sku, config)
    return basket

def apply_discount(basket, sku, config):
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
