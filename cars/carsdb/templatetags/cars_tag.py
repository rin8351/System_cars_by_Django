from django import template
from carsdb.models import *

register=template.Library()

@register.simple_tag()
def price_count(cn):
    part_list = car_part.objects.filter(part=cn)
    parts_list2 = parts.objects.filter(id__in=part_list.values('part'))
    for part in parts_list2:
        price = part.price * part.count_p
    return price