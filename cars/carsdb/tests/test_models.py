from django.contrib.auth import get_user_model
from django.test import TestCase

from carsdb.models import car_part, cars, parts

User = get_user_model()


class PartsModelTests(TestCase):
    def test_str_returns_model_name(self):
        part = parts.objects.create(
            type='Engine',
            price=1000,
            model_p='V8-500',
            count_p=1,
            params='500hp',
        )
        self.assertEqual(str(part), 'V8-500')

    def test_part_can_have_author(self):
        user = User.objects.create_user(username='anna', password='pass12345')
        part = parts.objects.create(
            type='Body',
            price=500,
            model_p='Sedan-A',
            count_p=1,
            params='steel',
            author=user,
        )
        self.assertEqual(part.author, user)


class CarsPriceCalculationTests(TestCase):
    """Price = sum(part.price * part.count_p) * (1 + margin / 100)."""

    def setUp(self):
        self.engine = parts.objects.create(
            type='Engine',
            price=100,
            model_p='Engine-100',
            count_p=2,
            params='test',
        )
        self.wheel = parts.objects.create(
            type='Wheel',
            price=50,
            model_p='Wheel-50',
            count_p=4,
            params='test',
        )

    def _link_parts(self, car, *part_list):
        for part in part_list:
            car_part.objects.create(car=car, part=part, name=car.name)
            car.parts.add(part)

    def test_price_recalculated_on_save_with_parts(self):
        # parts cost: 100*2 + 50*4 = 400; margin 10% → 440
        car = cars.objects.create(name='TestCar', margin=10)
        self._link_parts(car, self.engine, self.wheel)
        car.save()
        car.refresh_from_db()
        self.assertEqual(car.price, 440)

    def test_zero_margin_keeps_parts_sum(self):
        car = cars.objects.create(name='NoMargin', margin=0)
        self._link_parts(car, self.engine)
        car.save()
        car.refresh_from_db()
        # 100 * 2 * 1.0 = 200
        self.assertEqual(car.price, 200)

    def test_price_updates_when_part_price_changes(self):
        car = cars.objects.create(name='SignalCar', margin=0)
        self._link_parts(car, self.engine)
        car.save()
        car.refresh_from_db()
        self.assertEqual(car.price, 200)

        self.engine.price = 150
        self.engine.save()  # triggers signal
        car.refresh_from_db()
        # 150 * 2 = 300
        self.assertEqual(car.price, 300)

    def test_price_updates_when_part_link_removed(self):
        car = cars.objects.create(name='UnlinkCar', margin=0)
        self._link_parts(car, self.engine, self.wheel)
        car.save()
        car.refresh_from_db()
        self.assertEqual(car.price, 400)

        car_part.objects.filter(car=car, part=self.wheel).delete()
        car.refresh_from_db()
        # only engine left: 100 * 2 = 200
        self.assertEqual(car.price, 200)

    def test_str_returns_car_name(self):
        car = cars.objects.create(name='MyCar', margin=5)
        self.assertEqual(str(car), 'MyCar')


class CarPartModelTests(TestCase):
    def test_unique_together_car_and_part(self):
        from django.db import IntegrityError

        part = parts.objects.create(
            type='Engine',
            price=100,
            model_p='E1',
            count_p=1,
            params='x',
        )
        car = cars.objects.create(name='C1', margin=5)
        car_part.objects.create(car=car, part=part, name=car.name)

        with self.assertRaises(IntegrityError):
            car_part.objects.create(car=car, part=part, name=car.name)
