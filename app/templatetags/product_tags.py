import math
from django import template

register = template.Library()

@register.simple_tag
def calc_sell_price(price, Discount):
    if Discount is None or Discount == 0:
        return price
    sellprice = price - (price * Discount / 100)
    return math.floor(sellprice)

@register.simple_tag
def progress_bar(total_quantity, availability):
    try:
        total_quantity = int(total_quantity)
        availability = int(availability)
    except ValueError:
        return 0

    if total_quantity == 0:
        return 0

    progress = availability * (100 / total_quantity)
    return math.floor(progress)
