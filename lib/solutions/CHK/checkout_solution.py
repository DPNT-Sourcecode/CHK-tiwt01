""" Diary
* 2024-09-07 Sun
** 0935

On starting this morning there was an alert:

  IMPORTANT! You are not allowed to work on the solution while the challenge is PAUSED.

This wasn't anywhere in the documentation.  I did ~60 mins last night, pencil & paper sketches and refactoring.

** 1013

The `./record_and_upload.sh --no-video` scripts seems to stop after a while.

"""

PRICES = {
    'A': 50,
    'B': 30,
    'C': 20,
    'D': 15,
    'E': 40,
    'F': 10,
    'G': 20,
    'H': 10,
    'I': 35,
    'J': 60,
    'K': 70,
    'L': 90,
    'M': 15,
    'N': 40,
    'O': 10,
    'P': 50,
    'Q': 30,
    'R': 50,
    'S': 20,
    'T': 20,
    'U': 40,
    'V': 50,
    'W': 20,
    'X': 17,
    'Y': 20,
    'Z': 21,
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

def free_partner(basket, _, context):
    trigger_amount = context['amount']
    sku = context['main_sku']
    partner = context['partner_sku']
    while basket.to_pay_for.get(sku, 0) >= trigger_amount:
        basket.to_pay_for[sku] -= trigger_amount
        basket.paid_for.setdefault(sku, 0)
        basket.paid_for[sku] += trigger_amount
        basket.price += PRICES[sku] * trigger_amount
        pa = basket.to_pay_for.get(partner, 0)
        if pa:
            basket.to_pay_for[partner] -= 1
            basket.paid_for.setdefault(partner, 0)
            basket.paid_for[partner] += 1
    return basket
        
# '*' discounts are "whole basket" discounts
DISCOUNTS = {
    'A': [(multiple_price, {'amount': 3, 'price': 130}),
          (multiple_price, {'amount': 5, 'price': 200}),
          ],
    'B': [(multiple_price, {'amount': 2, 'price': 45})],
    'F': [(multiple_price, {'amount': 3, 'price': 20})],
    'H': [(multiple_price, {'amount': 5, 'price': 45}),
          (multiple_price, {'amount': 10, 'price': 80}),
          ],
    'K': [(multiple_price, {'amount': 2, 'price': 120})],
    'P': [(multiple_price, {'amount': 5, 'price': 200})],
    'Q': [(multiple_price, {'amount': 3, 'price': 80})],
    'U': [(multiple_price, {'amount': 3, 'price': 80})],
    'V': [(multiple_price, {'amount': 2, 'price': 90}),
          (multiple_price, {'amount': 3, 'price': 130}),
          ],
    '*': ((free_partner, {'amount': 2, 'main_sku': 'E', 'partner_sku': 'B'}),
          (free_partner, {'amount': 3, 'main_sku': 'N', 'partner_sku': 'M'}),          
          (free_partner, {'amount': 3, 'main_sku': 'R', 'partner_sku': 'Q'}),          
          )
    }

# | S    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
# | T    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
# | X    | 17    | buy any 3 of (S,T,X,Y,Z) for 45 |
# | Y    | 20    | buy any 3 of (S,T,X,Y,Z) for 45 |
# | Z    | 21    | buy any 3 of (S,T,X,Y,Z) for 45 |

# noinspection PyUnusedLocal
# skus = unicode string
def checkout(skus):
    if not valid(skus):
        return -1
    order = parse_skus(skus)
    basket = Basket(order)
    ds = applicable_discounts(basket)
    for dset in ds:
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
    # '*' discounts should be applied first
    return sorted([(sku, configs) for (sku,configs) in DISCOUNTS.items()
                   if sku == '*' or sku in basket.to_pay_for.keys()
                   ])

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
