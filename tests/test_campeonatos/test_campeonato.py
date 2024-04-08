from tests.test_setup import TestSetup
from django.urls import reverse
from tests.factories.campeonatos_test.campeonatos_factory import CampeoantoFactory
from rest_framework import status
import pdb



class CampeonatoTestCase(TestSetup):


    def test_list_campeonato(self):
        url='/campeonatos/'
        campeonato=CampeoantoFactory().create_campeoanto()
        response=self.client.get(
            url,
            headers={'Authorization':f"Bearer {self.token}"},
            format='JSON'
        )
        print("list")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)



    def test_detail_campeonato(self):
        url='/campeonatos/2/'
        campeonato=CampeoantoFactory().create_campeoanto()
        response=self.client.get(
            url,
            headers={'Authorization':f"Bearer {self.token}"},
            format='json'
        )
        #pdb.set_trace()
        print("detail")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_create_campeonato(self):
        url='/campeonatos/'
        campeonato=CampeoantoFactory().build_campeonato_JSON()
        response=self.client.post(
            url,
            campeonato,
            headers={'Authorization':f"Bearer {self.token}"},
            format='json'
        )
        #pdb.set_trace()
        print("create")
        print(response.data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
