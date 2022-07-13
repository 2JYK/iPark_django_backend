from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User as UserModel
from user.models import Region as RegionModel


# 회원가입 테스트
class UserRegistrationTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = RegionModel.objects.bulk_create([RegionModel(region_name="강남구"),
                                                      RegionModel(region_name="강동구"),
                                                      RegionModel(region_name="강북구")])

    def test_registration(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "birthday" : "2022-07-13",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 200)
        

# 로그인 테스트
class UserLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username" : "user10", "password" : "1010abc!"}
        cls.user = UserModel.objects.create_user("user10", "1010abc!")
        
    def test_login(self):
        url = reverse("token_obtain_pair")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!"
        }
        
        response = self.client.post(url, user_data)
        
        self.assertEqual(response.status_code, 200)
        
        
# 회원정보 수정 및 회원탈퇴 테스트
class UserInfoModifyDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.region = RegionModel.objects.bulk_create([RegionModel(region_name="강남구"),
                                                      RegionModel(region_name="강동구"),
                                                      RegionModel(region_name="강북구")])
        
        cls.user = UserModel.objects.create_user("user10", "1010abc!")
        cls.login_data = {"username": "user10", "password" : "1010abc!"}
        
    def setUp(self):
        self.access_token = self.client.post(reverse("token_obtain_pair"), self.login_data).data["access"]
    
    # 회원정보 수정 테스트
    def test_modify_user_info(self):
        url = reverse("user_view")
        data_for_change = {
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "birthday" : "2022-07-13",
            "region" : 3
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 200)
    
    # 회원탈퇴 테스트
    def test_delete_user(self):
        url = reverse("user_view")
        
        response = self.client.delete(url, HTTP_AUTHORIZATION=f"Bearer {self.access_token}")
        
        self.assertEqual(response.data["message"], "회원탈퇴 성공")
        
        
# 아이디 찾기 테스트
class SearchUsernameTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "birthday" : "2022-07-13",
        }
        cls.user = UserModel.objects.create(**user_data)
        
    def test_search_username(self):
        url = reverse("myid_view")
        data = {
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010"
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.data["username"], "user10")