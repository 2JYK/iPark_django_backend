from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User as UserModel
from user.models import Region as RegionModel


# 회원가입 테스트
class UserRegistrationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        region_data = ["강남구", "강서구", "강북구", "은평구", "동작구", "중구"]
        for region in region_data:
            cls.region = RegionModel.objects.create(region_name=region)
        
        cls.region.save()

    def test_registration_all_data(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["username"], "user10")
        self.assertEqual(response.data["region"], 2)
        
    