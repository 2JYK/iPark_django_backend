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
        
    # 중복 username인 경우
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
        
    # 이메일을 입력하지 않았을 때
    def test_registration_no_email(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user1010",
            "email" : "",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "이 필드는 blank일 수 없습니다.")
        
    # 입력한 이메일의 양식이 틀렸을 때
    def test_registration_wrong_email(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        user_data_2 = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10gmail.com",
            "phone" : "010-1010-1010",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)
        response_2 = self.client.post(url, user_data_2)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["email"][0], "유효한 이메일 주소를 입력하십시오.")
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.data["email"][0], "유효한 이메일 주소를 입력하십시오.")
        
    # 중복 이메일을 입력한 경우
    def test_registration_same_email(self):
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
            "username" : "user20",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user10@gmail.com",
            "phone" : "010-2020-2020",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)
        response_2 = self.client.post(url, user_data_2)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_2.status_code, 400)
        self.assertEqual(response_2.data["email"][0], "user의 이메일은/는 이미 존재합니다.")
        
    # 핸드폰 번호를 입력하지 않은 경우
    def test_registration_no_phone(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user1010",
            "email" : "user10@gmail.com",
            "phone" : "",
            "region" : 2
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["phone"][0], "이 필드는 blank일 수 없습니다.")
        
    # 존재하지 않는 지역을 입력한 경우
    def test_registration_wrong_region(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user1010",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 26
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["region"][0], '유효하지 않은 pk "26" - 객체가 존재하지 않습니다.')
        
    # 지역을 입력하지 않은 경우 (없어도 문제가 되지는 않지만, 프론트에서는 강남구가 기본값으로 설정되어 있어 선택하지 않을 일은 없음)
    def test_registration_no_region(self):
        url = reverse("user_view")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user1010",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010"
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 201)


# 로그인 테스트
class UserLoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username" : "user10", "password" : "1010abc!"}
        cls.user = UserModel.objects.create_user("user10", "1010abc!")
    
    # 모든 정보를 기입한 경우
    def test_login_all_data(self):
        url = reverse("ipark_token")
        user_data = {
            "username" : "user10",
            "password" : "1010abc!"
        }
        
        response = self.client.post(url, user_data)
        
        self.assertEqual(response.status_code, 200)
        
    # username을 기입하지 않은 경우
    def test_login_no_username(self):
        url = reverse("ipark_token")
        user_data = {
            "username" : "",
            "password" : "1010abc!"
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "이 필드는 blank일 수 없습니다.")