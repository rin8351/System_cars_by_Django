from django.contrib.auth import get_user_model
from django.test import TestCase

from carsdb.forms import AddCars, AddParts
from carsdb.models import car_part, cars, parts

User = get_user_model()


class AddPartsFormTests(TestCase):
    def test_valid_data(self):
        form = AddParts(
            data={
                'type': 'Engine',
                'model_p': 'V6',
                'price': 1000,
                'count_p': 1,
                'params': '250hp',
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_price_must_be_positive(self):
        form = AddParts(
            data={
                'type': 'Engine',
                'model_p': 'V6',
                'price': 0,
                'count_p': 1,
                'params': '250hp',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_negative_price_rejected(self):
        form = AddParts(
            data={
                'type': 'Engine',
                'model_p': 'V6',
                'price': -10,
                'count_p': 1,
                'params': '250hp',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)

    def test_quantity_must_be_positive(self):
        form = AddParts(
            data={
                'type': 'Engine',
                'model_p': 'V6',
                'price': 100,
                'count_p': 0,
                'params': '250hp',
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('count_p', form.errors)

    def test_required_fields(self):
        form = AddParts(data={})
        self.assertFalse(form.is_valid())
        for field in ('type', 'model_p', 'price', 'count_p', 'params'):
            self.assertIn(field, form.errors)


class AddCarsFormTests(TestCase):
    def setUp(self):
        self.part = parts.objects.create(
            type='Engine',
            price=100,
            model_p='E1',
            count_p=1,
            params='x',
        )

    def test_valid_data(self):
        form = AddCars(
            data={
                'name': 'Sedan',
                'margin': 15,
                'parts': [self.part.pk],
            }
        )
        self.assertTrue(form.is_valid(), form.errors)

    def test_margin_must_be_positive(self):
        form = AddCars(
            data={
                'name': 'Sedan',
                'margin': 0,
                'parts': [self.part.pk],
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn('margin', form.errors)

    def test_create_saves_car_and_part_links(self):
        form = AddCars(
            data={
                'name': 'Coupe',
                'margin': 10,
                'parts': [self.part.pk],
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        form.save()

        car = cars.objects.get(name='Coupe')
        self.assertEqual(car.margin, 10)
        self.assertTrue(car_part.objects.filter(car=car, part=self.part).exists())
        # parts cost 100*1, margin 10% → 110
        car.refresh_from_db()
        self.assertEqual(car.price, 110)
