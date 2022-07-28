from django.urls import reverse
from rest_framework.test import APITestCase

from park.models import Park as ParkModel
from park.models import Option as OptionModel
from user.models import User as UserModel


# 공원 댓글 테스트
class ParkCommentTest(APITestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {"username" : "sugisugi", "password" : "sugipassword"}
        cls.user = UserModel.objects.create_user("sugisugi", "sugipassword")
        cls.comment_data = {"username" : "sugisugi", "park" : 1, "comment" : "test_comment"}
        cls.park = ParkModel.objects.create(park_name = "park_name",
                                            addr = "addr",
                                            image = "image",
                                            list_content = "list_content",
                                            admintel = "admintel",
                                            longitude = "longitude",
                                            latitude = "latitude",
                                            main_equip = "main_equip",
                                            template_url = "template_url",
                                            updated_at = "updated_at",
                                            check_count = 10
                                        )
        
    def setUp(self):
        self.access_token = self.client.post(reverse('token_obtain_pair'), self.user_data).data['access']
    
    # 작성 : 로그인 X
    def test_fail_if_not_logged_in(self):
        url = reverse("park_comment_create", kwargs={'park_id':1})
        response = self.client.post(url, self.comment_data)
        self.assertEqual(response.status_code, 401)  
    
    # 작성 : 로그인 O
    def test_create_comment(self):
        response = self.client.post(
            path=reverse("park_comment_create", kwargs={'park_id':1}),
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )
        self.assertEqual(response.status_code, 200)
        
    # 작성 : 로그인 O 내용입력 X
    def test_fail_no_comment(self):
        response = self.client.post(
            path=reverse("park_comment_create", kwargs={'park_id':1}),
            data={"username" : "sugisugi",
                  "park" : 1, 
                  "comment" : ""},
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )
        self.assertEqual(response.status_code, 400)


# 공원 검색 페이지 테스트
class OptionTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        park_data = {
            "park_name": "서울대공원",
            "zone": "과천시",
            "image": "http://www.naver.com",
            "check_count": "5"
        }
        cls.park = ParkModel.objects.create(**park_data)
        
        option_list = ["조경", "놀이공원"]
        for option in option_list:
            cls.option_obj = OptionModel.objects.create(option_name=option)
            cls.park.option.add(cls.option_obj)

        cls.park.save()

    # 공원 옵션만 들어올 경우
    def test_option_find(self):
        url = reverse("park_search")
        response = self.client.get(f'{url}?param=1&param=2')
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")
    
    # 공원 지역만 들어올 경우
    def test_zone_find(self):
        url = reverse("park_search")
        response = self.client.get(f'{url}?param=과천시')
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")
    
    # 공원 옵션과 지역 모두 들어올 경우
    def test_option_and_zone_find(self):
        url = reverse("park_search")
        response = self.client.get(f'{url}?param=2&param=과천시')
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")


# 인기순 공원 검색 테스트
class ParkPopularityTest(APITestCase):
    def setUp(self):
        self.option_obj = OptionModel.objects.create(option_name="조경")

        park_list = [{"park_name": "남산공원", "check_count": "8"}, 
                     {"park_name": "서울대공원", "check_count": "4"},
                     {"park_name": "보라매근린공원", "check_count": "10"},
                     {"park_name": "길동생태공원", "check_count": "0"}]

        for park_data in park_list:
            self.park = ParkModel.objects.create(**park_data)
            self.park.option.add(self.option_obj)
            self.park.save()   
    
    def test_popularity_park(self):
        url = reverse("park_popularity")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        
        
# 토글 공원 리스트 테스트
class ToggleParkListTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.park = ParkModel.objects.create(park_name = "강남공원",
                                            addr = "서울특별시 강남구",
                                            zone = "강남구",
                                            image = "http://www.gangnampark.com/parkimg",
                                            list_content = "강남구에 있는 공원이다.",
                                            admintel = "02-333-4444",
                                            longitude = "126.1232144",
                                            latitude = "37.1111111",
                                            main_equip = "운동기구 화장실 지하철역",
                                            template_url = "http://www.gangnampark.com/",
                                        )
                
    def test_get_toggle_list(self):
        url = reverse("toggle_park")
        response = self.client.get(url)
        
        self.assertEqual(response.data[0]["park_name"], "강남공원")
        self.assertEqual(response.status_code, 200)