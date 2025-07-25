from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from http.cookies import SimpleCookie
from rest_framework.test import APITestCase

class RegistrationTests(APITestCase):
	def test_create_registration(self):
		url = reverse('registration-list')
		data = {
			"email": "martha@mail.de",
			"password": "123456789",
			"confirmed_password": "123456789",
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class LoginTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='martha@gmail.com', email='martha@gmail.com', password='123456789')

		# Authentication with token
		self.client.cookies = SimpleCookie({'access_token': 'hgdjkghsiojsifjsigigshuhfie'})

	def test_create_login(self):
		url = reverse('token_obtain_pair')
		data = {
			"username": "martha@gmail.com",
			"email": "martha@gmail.com",
			"password": "123456789"
		}
		response = self.client.post(url, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)