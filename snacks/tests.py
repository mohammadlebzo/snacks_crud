from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db.models import CharField, ForeignKey, TextField

from .models import Snack


# Create your tests here.
class SnacksTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test', email='test@@test.com',
            password='test@12345'
        )
        self.snack = Snack.objects.create(
            name="Test",
            purchaser=self.user,
            description="Testing Text",
        )

    def test_view_status(self):
        data = {
            "name": "Test Create",
            "purchaser": self.user.id
        }

        list_response = self.client.get(reverse('snack_list'))
        detail_response = self.client.get(reverse('snack_detail', args=[self.snack.id]))
        create_response = self.client.post(path=reverse('snack_create'), data=data, follow=True)
        update_response = self.client.post(path=reverse('snack_update', args=[self.snack.id]), data=data, follow=True)
        delete_response = self.client.post(path=reverse('snack_delete', args=[self.snack.id]), follow=True)

        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(detail_response.status_code, 200)
        self.assertEqual(create_response.status_code, 200)
        self.assertEqual(update_response.status_code, 200)
        self.assertEqual(delete_response.status_code, 200)

    def test_view_template(self):
        data = {
            "name": "Test Create",
            "purchaser": self.user.id
        }

        list_response = self.client.get(reverse('snack_list'))
        detail_response = self.client.get(reverse('snack_detail', args=[self.snack.id]))
        create_response = self.client.post(path=reverse('snack_create'), data=data, follow=True)
        update_response = self.client.post(path=reverse('snack_update', args=[self.snack.id]), data=data, follow=True)
        delete_response = self.client.post(path=reverse('snack_delete', args=[self.snack.id]), follow=True)

        self.assertTemplateUsed(list_response, 'snack_list.html')
        self.assertTemplateUsed(detail_response, 'snack_detail.html')
        self.assertTemplateUsed(create_response, 'snack_detail.html')
        self.assertTemplateUsed(update_response, 'snack_detail.html')
        self.assertTemplateUsed(delete_response, 'snack_list.html')

    def test_after_create_view_and_delete_view_array_length(self):
        data = {
            "name": "Test Create",
            "purchaser": self.user.id
        }

        self.client.post(path=reverse('snack_create'), data=data, follow=True)
        self.assertEqual(len(Snack.objects.all()), 2)

        self.client.post(path=reverse('snack_delete', args=[2]), follow=True)
        self.assertEqual(len(Snack.objects.all()), 1)

    def test_model_str_method(self):
        self.assertEqual(str(self.snack), 'Test')

    def test_model_fields(self):
        field_name = Snack._meta.get_field("name")
        field_purchaser = Snack._meta.get_field("purchaser")
        field_description = Snack._meta.get_field("description")

        self.assertTrue(isinstance(field_name, CharField))
        self.assertTrue(isinstance(field_purchaser, ForeignKey))
        self.assertTrue(isinstance(field_description, TextField))

