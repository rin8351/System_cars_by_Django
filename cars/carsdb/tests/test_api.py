from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from carsdb.models import parts

User = get_user_model()


class PartsAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('api-parts-list')
        self.part = parts.objects.create(
            type='Engine',
            price=1000,
            model_p='V8-500',
            count_p=1,
            params='500hp',
        )
        self.user = User.objects.create_user(username='apiuser', password='pass12345')

    def _detail_url(self, pk):
        return reverse('api-parts-detail', kwargs={'pk': pk})

    def _grant(self, codename):
        perm = Permission.objects.get(codename=codename)
        self.user.user_permissions.add(perm)

    def test_list_parts_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        models = [item['model_p'] for item in response.data['results']]
        self.assertIn('V8-500', models)

    def test_retrieve_part_public(self):
        response = self.client.get(self._detail_url(self.part.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['model_p'], 'V8-500')
        self.assertEqual(response.data['price'], 1000)

    def test_search_parts(self):
        parts.objects.create(
            type='Wheel', price=50, model_p='Other', count_p=4, params='y'
        )
        response = self.client.get(self.list_url, {'search': 'V8'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        models = [item['model_p'] for item in response.data['results']]
        self.assertIn('V8-500', models)
        self.assertNotIn('Other', models)

    def test_create_requires_permission(self):
        payload = {
            'type': 'Body',
            'model_p': 'Sedan',
            'price': 200,
            'count_p': 1,
            'params': 'steel',
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_part_with_permission(self):
        self._grant('add_parts')
        self.client.force_authenticate(user=self.user)
        payload = {
            'type': 'Body',
            'model_p': 'Sedan-API',
            'price': 200,
            'count_p': 1,
            'params': 'steel',
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['model_p'], 'Sedan-API')
        self.assertEqual(response.data['author'], 'apiuser')
        self.assertTrue(parts.objects.filter(model_p='Sedan-API', author=self.user).exists())

    def test_create_rejects_non_positive_price(self):
        self._grant('add_parts')
        self.client.force_authenticate(user=self.user)
        payload = {
            'type': 'Body',
            'model_p': 'Bad',
            'price': 0,
            'count_p': 1,
            'params': 'x',
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_update_part_with_permission(self):
        self._grant('change_parts')
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            self._detail_url(self.part.pk),
            {'price': 1500},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.part.refresh_from_db()
        self.assertEqual(self.part.price, 1500)

    def test_delete_part_with_permission(self):
        self._grant('delete_parts')
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self._detail_url(self.part.pk))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(parts.objects.filter(pk=self.part.pk).exists())
