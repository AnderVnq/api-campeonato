from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker 
from django.contrib.auth.models import User
import time

class TestSetup(APITestCase):
    
    def setUp(self):
        

        faker = Faker()
        self.login_url='/login/'
        self.user=User.objects.create_superuser(
            username='testdev',
            password='heaveny2',
            email=faker.email()
        )
        response=self.client.post(
            self.login_url,
            {
                'username':self.user.username,
                'password':'heaveny2'
            },
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        #import pdb; pdb.set_trace()
        self.token=response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+self.token)
        return super().setUp()


    def test_asd(self):
        print(self.token)