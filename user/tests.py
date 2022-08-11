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

    # 정상적인 회원가입
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
        
    # username이 없을 때
    def test_registration_no_username(self):
        url = reverse("user_view")
        user_data = {
            "username" : "",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "이 필드는 blank일 수 없습니다.")
        
    # username의 자릿수가 모자랄 때
    def test_registration_wrong_username(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "username의 길이는 6자리 이상이어야 합니다.")
        
    # 중복 username일 때의 회원가입 테스트
    def test_registration_same_username(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        user_data_2 = {
            "username" : "user10",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-2020-2020",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)
        response_2 = self.client.post(url, user_data_2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.data["username"][0], "user의 사용자 계정은/는 이미 존재합니다.")

    # 비밀번호를 입력하지 않았을 때
    def test_registration_no_password(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "이 필드는 blank일 수 없습니다.")
        
    # 입력한 비밀번호의 양식이 틀렸을 때
    def test_registration_wrong_password(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010a",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "비밀번호는 8 자리 이상이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다.")
        
    # 이름을 입력하지 않았을 때
    def test_registration_no_fullname(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["fullname"][0], "이 필드는 blank일 수 없습니다.")