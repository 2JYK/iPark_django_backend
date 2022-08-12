from django.contrib.auth.hashers import make_password
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
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
    
    # password를 기입하지 않은 경우
    def test_login_no_password(self):
        url = reverse("ipark_token")
        user_data = {
            "username" : "user1010",
            "password" : ""
        }
        
        response = self.client.post(url, user_data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "이 필드는 blank일 수 없습니다.")
        
        
# 회원정보 수정 및 회원탈퇴 테스트
""" 
회원정보를 수정할 때, 두 가지의 경우로 나누어진다. 
1. 비밀번호를 제외한 정보들만 변경할 때
2. 비밀번호까지 전부 다 변경할 떄

회원정보를 변경할 때 partial=True로 인해 변경하고 싶은 정보만 변경할 수 있다. 
하지만 이 경우에는 빈 값을 넣으면 기본 validator에 의해 걸러지기 때문에 원래 가지고 있던 값을 넣어줘야 한다. 
"""
class UserInfoModifyDeleteTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        region_data = ["강남구", "강서구", "강북구", "은평구", "동작구", "중구"]
        for region in region_data:
            cls.region = RegionModel.objects.create(region_name=region)
        
        cls.region.save()
        
        cls.user = UserModel.objects.create(
            username="user10",
            password=make_password("1010abc!"),
            fullname="user10",
            email="user10@gmail.com",
            phone="010-1010-1010",
            region=RegionModel.objects.get(id=3))
        
        cls.user_1 = UserModel.objects.create(
            username="user30",
            password=make_password("3030abc!"),
            fullname="user30",
            email="user30@gmail.com",
            phone="010-3030-3030",
            region=RegionModel.objects.get(id=3))

        cls.client = APIClient()
        cls.login_data = {"username": "user10", "password" : "1010abc!"}
 
        cls.access_token = cls.client.post(reverse("ipark_token"), cls.login_data).data["access"]
        
    # 회원정보 수정 테스트(모든 데이터 수정)
    def test_modify_all_user_info(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 201)
    
    # username만 변경될 때
    def test_modify_only_username(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 201)
        
    # username이 없을 때
    def test_modify_no_username(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "이 필드는 blank일 수 없습니다.")
        
    # username의 자릿수가 모자랄 때
    def test_modify_wrong_username(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "username의 길이는 6자리 이상이어야 합니다.")
        
    # username이 중복될 때
    def test_modify_same_username(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user30",
            "password" : "2020abc!",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["username"][0], "user의 사용자 계정은/는 이미 존재합니다.")
    
    # password만 변경할 때
    def test_modify_only_password(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user10",
            "password" : "2020abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 3
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 201)
    
    # password가 없을 때
    def test_modify_no_password(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "password" : "",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "이 필드는 blank일 수 없습니다.")
        
    # password의 양식이 틀렸을 때
    def test_modify_wrong_password(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "password" : "2020ab",
            "fullname" : "user20",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"][0], "비밀번호는 8 자리 이상이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다.")
    
    # password가 중복될 때
    def test_modify_same_password(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user10",
            "password" : "1010abc!",
            "fullname" : "user10",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["password"], "현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다.")
    
    # fullname만 변경할 때
    def test_modify_only_fullname(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user10",
            "fullname" : "user20",
            "email" : "user10@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 3
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["fullname"], "user20")

    # fullname이 없을 때
    def test_modify_no_fullname(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "password" : "2020abc!",
            "fullname" : "",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["fullname"][0], "이 필드는 blank일 수 없습니다.")
        
    # fullname의 자릿수 테스트 (현재 걸어놓은 제약이 없음)
    def test_modify_fullname_no_limit(self):
        url = reverse("user_view")
        data_for_change = {
            "username" : "user20",
            "password" : "2020abc!",
            "fullname" : "us",
            "email" : "user20@gmail.com",
            "phone" : "010-1010-1010",
            "region" : 4
        }
        
        response = self.client.put(
            path=url, 
            data=data_for_change,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["fullname"], "us")