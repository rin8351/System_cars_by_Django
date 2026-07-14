from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from carsdb.models import cars, parts

User = get_user_model()


class PublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_ok(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_parts_list_ok(self):
        parts.objects.create(
            type='Engine',
            price=100,
            model_p='E1',
            count_p=1,
            params='x',
        )
        response = self.client.get(reverse('parts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'E1')

    def test_cars_list_ok(self):
        cars.objects.create(name='DemoCar', margin=10, price=0)
        response = self.client.get(reverse('cars'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'DemoCar')

    def test_parts_search_filters_results(self):
        parts.objects.create(
            type='Engine', price=100, model_p='FindMe', count_p=1, params='x'
        )
        parts.objects.create(
            type='Wheel', price=50, model_p='Other', count_p=4, params='y'
        )
        response = self.client.get(reverse('parts'), {'q': 'FindMe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FindMe')
        self.assertNotContains(response, 'Other')


class PermissionViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='worker', password='pass12345')
        self.part = parts.objects.create(
            type='Engine',
            price=100,
            model_p='E1',
            count_p=1,
            params='x',
        )
        self.car = cars.objects.create(name='Car1', margin=10)

    def _grant(self, codename):
        perm = Permission.objects.get(codename=codename)
        self.user.user_permissions.add(perm)

    def test_add_parts_requires_login(self):
        response = self.client.get(reverse('add_parts'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)

    def test_add_parts_forbidden_without_permission(self):
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('add_parts'))
        self.assertEqual(response.status_code, 403)

    def test_add_parts_allowed_with_permission(self):
        self._grant('add_parts')
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('add_parts'))
        self.assertEqual(response.status_code, 200)

    def test_add_cars_forbidden_without_permission(self):
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('add_cars'))
        self.assertEqual(response.status_code, 403)

    def test_add_cars_allowed_with_permission(self):
        self._grant('add_cars')
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('add_cars'))
        self.assertEqual(response.status_code, 200)

    def test_edit_parts_requires_permission(self):
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('edit_parts', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 403)

        self._grant('change_parts')
        response = self.client.get(reverse('edit_parts', kwargs={'pk': self.part.pk}))
        self.assertEqual(response.status_code, 200)

    def test_delete_cars_requires_permission(self):
        self.client.login(username='worker', password='pass12345')
        response = self.client.get(reverse('delete_cars', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 403)

        self._grant('delete_cars')
        response = self.client.get(reverse('delete_cars', kwargs={'pk': self.car.pk}))
        self.assertEqual(response.status_code, 200)

    def test_add_part_via_post_sets_author(self):
        self._grant('add_parts')
        self.client.login(username='worker', password='pass12345')
        response = self.client.post(
            reverse('add_parts'),
            {
                'type': 'Body',
                'model_p': 'NewBody',
                'price': 200,
                'count_p': 1,
                'params': 'metal',
            },
        )
        self.assertEqual(response.status_code, 302)
        created = parts.objects.get(model_p='NewBody')
        self.assertEqual(created.author, self.user)
