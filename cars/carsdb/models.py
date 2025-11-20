from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

class parts(models.Model):
    type = models.CharField(max_length = 100)
    price = models.IntegerField()
    model_p = models.CharField(max_length = 100)
    count_p = models.IntegerField()
    params = models.CharField(max_length = 100)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, 
                               null=True, default=None, related_name='parts_author')

    def __str__(self):
        return self.model_p

    def get_absolute_url(self):
        return reverse('parts')

class cars(models.Model):
    name = models.CharField(max_length=100)
    parts = models.ManyToManyField(parts, related_name='carss')
    margin = models.IntegerField()
    price = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cars')

    def save(self, *args, **kwargs):
        if self.pk is not None:
            try:
                part_list = car_part.objects.filter(car=self)
                parts_list2 = parts.objects.filter(id__in=part_list.values('part'))
                price = 0
                for part in parts_list2:
                    # Проверяем, что price и count_p существуют и корректны
                    if part.price is not None and part.count_p is not None:
                        price += part.price * part.count_p
                
                # Проверяем, что margin не None
                if self.margin is not None:
                    self.price = int(price * (1 + self.margin / 100))
                else:
                    self.price = int(price)
            except (ValueError, TypeError, ZeroDivisionError) as e:
                # В случае ошибки устанавливаем цену в 0
                self.price = 0
        super().save(*args, **kwargs)


class car_part(models.Model):
    car = models.ForeignKey(cars, on_delete=models.CASCADE)
    part = models.ForeignKey(parts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ['car', 'part']

    def __str__(self):
        return "{} {}".format(self.car.__str__(), self.part.__str__())