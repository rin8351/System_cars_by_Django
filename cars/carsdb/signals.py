from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import parts, cars, car_part


def recalculate_car_price(car):
    """Пересчитывает цену автомобиля на основе связанных деталей"""
    part_list = car_part.objects.filter(car=car)
    parts_list2 = parts.objects.filter(id__in=part_list.values('part'))
    price = 0
    for part in parts_list2:
        price += part.price * part.count_p
    new_price = price * (1 + car.margin / 100)
    # Используем update() напрямую, чтобы избежать вызова метода save() модели
    cars.objects.filter(pk=car.pk).update(price=new_price)


@receiver(post_save, sender=parts)
def update_car_prices_on_part_change(sender, instance, created, **kwargs):
    """Пересчитывает цены всех автомобилей, использующих измененную деталь"""
    # Пересчитываем цены для всех автомобилей, использующих эту деталь
    # Это срабатывает при создании (created=True) и при обновлении (created=False)
    # При обновлении пересчитываем всегда, так как могла измениться цена или количество
    related_cars = cars.objects.filter(parts=instance)
    for car in related_cars:
        recalculate_car_price(car)


@receiver(post_delete, sender=car_part)
def update_car_price_on_part_removal(sender, instance, **kwargs):
    """Пересчитывает цену автомобиля после удаления связи с деталью"""
    recalculate_car_price(instance.car)

