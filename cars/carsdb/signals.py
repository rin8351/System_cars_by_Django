from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import parts, cars, car_part


def recalculate_car_price(car):
    """Recalculates car price based on linked parts."""
    part_list = car_part.objects.filter(car=car)
    parts_list2 = parts.objects.filter(id__in=part_list.values('part'))
    price = 0
    for part in parts_list2:
        price += part.price * part.count_p
    new_price = price * (1 + car.margin / 100)
    # Use update() directly to avoid calling the model save() method
    cars.objects.filter(pk=car.pk).update(price=new_price)


@receiver(post_save, sender=parts)
def update_car_prices_on_part_change(sender, instance, created, **kwargs):
    """Recalculates prices for all cars that use the changed part."""
    # Triggers on create and update; on update always recalculate
    # because price or quantity may have changed
    related_cars = cars.objects.filter(parts=instance)
    for car in related_cars:
        recalculate_car_price(car)


@receiver(post_delete, sender=car_part)
def update_car_price_on_part_removal(sender, instance, **kwargs):
    """Recalculates car price after a part link is removed."""
    recalculate_car_price(instance.car)
