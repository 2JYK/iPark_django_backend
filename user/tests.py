from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User
from user.models import Region


# 회원가입 테스트
class UserRegistrationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region_data = {"region_name": "강남구", "region_name": "강동구", "region_name": "강북구"}
        cls.region = Region.objects.create(**cls.region_data)
        
    def test_registration(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "101010",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "birthday" : "2022-07-13",
            "region" : 1
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 200)
        

# 로그인 테스트
class UserLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username" : "user10", "password" : "101010"}
        cls.user = User.objects.create_user("user10", "101010")
        
    def test_login(self):
        url = reverse("token_obtain_pair")
        user_data = {
            "username" : "user10",
            "password" : "101010"
        }
        
        response = self.client.post(url, user_data)
        
        self.assertEqual(response.status_code, 200)