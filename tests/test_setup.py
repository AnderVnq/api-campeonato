from rest_framework.test import APITestCase
from rest_framework import status
from faker import Faker 








class TestSetup(APITestCase):
    
    def setUp(self):
        from django.contrib.auth.models import User

        faker = Faker()

        self.login_url='/login/'
        self.user=User.objects.create_superuser(
            username='testdev',
            password='heaveny2',
            first_name='testdev',
            last_name='dev',
            email=faker.email()
        )
        response=self.client.post(
            self.login_url,
            {
                'username':self.user.username,
                'password':self.user.password
            },
            format='json'
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        import pdb; pdb.set_trace()
        # self.token=response.data['token']
        # self.client.credemtials(HTTP_AUTHORIZATION='Bearer '+self.token)
        return super().setUp()


    def test_asd():
        pass