from django.test import Client
from django.test import TestCase
from faker import Faker
from usersapp.models import ParserUser

class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.fake = Faker()


    def test_statuses(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('results/')
        self.assertEqual(response.status_code, 404)

    def test_login_required(self):
        ParserUser.objects.create_user(username='test_user', email='test@test.com', password='leo1234567')
        response = self.client.get('results/')
        self.assertEqual(response.status_code, 404)

        self.client.login(username='test_user', password='leo1234567')

        response = self.client.get('/result/')
        self.assertEqual(response.status_code, 404)