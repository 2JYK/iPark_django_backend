from django.urls import reverse
from rest_framework.test import APITestCase

from park.models import Park as ParkModel
from park.models import Option as OptionModel
from park.models import ParkOption as ParkOptionModel
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
        self.access_token = self.client.post(reverse('ipark_token'), self.user_data).data['access']
    
    def test_get_park_comments(self):
        url = reverse("park_comment_create", kwargs={'park_id':1})
        response = self.client.get(url, self.comment_data)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_create_comment_if_not_logged_in(self):
        url = reverse("park_comment_create", kwargs={'park_id':1})
        response = self.client.post(url, self.comment_data)
        self.assertEqual(response.status_code, 401)  
    
    def test_successful_create_comment(self):
        response = self.client.post(
            path=reverse("park_comment_create", kwargs={'park_id':1}),
            data=self.comment_data,
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
            )
        self.assertEqual(response.status_code, 200)
        
    def test_fail_create_comment_no_content(self):
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
    def create_park(self, park_data, option_list):
        # optionmodel 생성
        self.options = ["조경", "운동", "놀이공원", "역사", "학습테마", "교양", "편익", "주차장"]
        for option in self.options:
            self.option_model = OptionModel.objects.create(option_name=option)

        self.option_model.save()
        
        self.park = ParkModel.objects.create(**park_data)

        # through table을 활용해 공원과 옵션값을 매치시켜줌
        for option in option_list:
            ParkOptionModel.objects.create(park=self.park, option=OptionModel.objects.get(id=option))

        self.park.save()

    @classmethod
    def setUpTestData(cls):        
        park_data_1 = {
            "park_name": "서울대공원",
            "zone": "과천시",
            "image": "1",
            "check_count": "5"
        }
        option_list_1 = [1, 2, 3]
        
        park_data_2 = {
            "park_name": "남산공원",
            "zone": "중구",
            "image": "2",
            "check_count": "10"
        }
        option_list_2 = [1, 2, 4, 5, 7, 8]
        
        park_data_3 = {
            "park_name": "간데메공원",
            "zone": "동대문구",
            "image": "3",
            "check_count": "1"
        }
        option_list_3 = [1, 2, 7]

        cls.create_park(cls, park_data_1, option_list_1)
        cls.create_park(cls, park_data_2, option_list_2)
        cls.create_park(cls, park_data_3, option_list_3)

    # 공원 옵션만 들어올 경우(성공)
    def test_option_find(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=1&param=2&param=3")
        response_2 = self.client.get(f"{url}?param=4&param=8")
        response_3 = self.client.get(f"{url}?param=7")

        self.assertEqual(response.data[0]["park_name"], "서울대공원")
        self.assertEqual(response.data[1]["park_name"], "남산공원")
        self.assertEqual(response.data[2]["park_name"], "간데메공원")
        self.assertEqual(response_2.data[0]["park_name"], "남산공원")
        self.assertEqual(response_3.data[0]["park_name"], "남산공원")
        self.assertEqual(response_3.data[1]["park_name"], "간데메공원")
        
    # 공원 옵션만 들어올 경우(실패)
    def test_option_find_fail(self):
        url = reverse("park_search")
        # 전체 옵션 리스트에 아예 없는 옵션
        response = self.client.get(f"{url}?param=9")
        # 전체 옵션 리스트에는 있지만 공원들이 갖고 있지 않은 옵션
        response_1 = self.client.get(f"{url}?param=6")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_1.data["message"], "공원을 찾을 수 없습니다.")
    
    # 공원 지역만 들어올 경우(성공)
    def test_zone_find(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=과천시")
        response_2 = self.client.get(f"{url}?param=중구")
        response_3 = self.client.get(f"{url}?param=동대문구")
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")
        self.assertEqual(response_2.data[0]["park_name"], "남산공원")
        self.assertEqual(response_3.data[0]["park_name"], "간데메공원")
    
    # 공원 지역만 들어올 경우(실패)
    def test_zone_find_fail(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=강남구")
        response_2 = self.client.get(f"{url}?param=은평구")
        response_3 = self.client.get(f"{url}?param=강서구")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(response_3.data["message"], "공원을 찾을 수 없습니다.")
        
    # 공원 옵션과 지역 모두 들어올 경우(성공)
    def test_option_and_zone_find(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=2&param=과천시")
        response_2 = self.client.get(f"{url}?param=4&param=중구")
        response_3 = self.client.get(f"{url}?param=1&param=7&param=동대문구")
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")
        self.assertEqual(response_2.data[0]["park_name"], "남산공원")
        self.assertEqual(response_3.data[0]["park_name"], "간데메공원")
    
    # 공원 옵션과 지역 모두 들어올 경우(실패)
    def test_option_and_zone_find_fail(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=6&param=과천시")
        response_2 = self.client.get(f"{url}?param=3&param=중구")
        response_3 = self.client.get(f"{url}?param=3&param=6&param=동대문구")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_2.status_code, 404)
        self.assertEqual(response_3.data["message"], "공원을 찾을 수 없습니다.")
    
    # 공원 이름으로 검색(성공)    
    def test_park_by_name(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=서")
        response_2 = self.client.get(f"{url}?param=원")

        self.assertEqual(response.data[0]["park_name"], "서울대공원")
        self.assertEqual(response_2.data[0]["park_name"], "서울대공원")
        self.assertEqual(response_2.data[1]["park_name"], "남산공원")
        self.assertEqual(response_2.data[2]["park_name"], "간데메공원")
        
    # 공원 이름으로 검색(실패)    
    def test_park_by_name_fail(self):
        url = reverse("park_search")
        response = self.client.get(f"{url}?param=탑골공원")
        response_2 = self.client.get(f"{url}?param=상도근린공원")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_2.data["message"], "공원을 찾을 수 없습니다.")


# 인기순 공원 검색 테스트
class ParkPopularityTest(APITestCase):
    def create_park(self, park_data):        
        self.park = ParkModel.objects.create(**park_data)

        self.park.save()

    @classmethod
    def setUpTestData(cls):        
        park_data_1 = {
            "park_name": "서울대공원",
            "zone": "과천시",
            "image": "1",
            "check_count": "5"
        }
        
        park_data_2 = {
            "park_name": "남산공원",
            "zone": "중구",
            "image": "2",
            "check_count": "10"
        }
        
        park_data_3 = {
            "park_name": "간데메공원",
            "zone": "동대문구",
            "image": "3",
            "check_count": "1"
        }
        
        park_data_4 = {
            "park_name": "효창공원",
            "zone": "용산구",
            "image": "4",
            "check_count": "0"
        }

        cls.create_park(cls, park_data_1)
        cls.create_park(cls, park_data_2)
        cls.create_park(cls, park_data_3)
        cls.create_park(cls, park_data_4)
    
    def test_popularity_park(self):
        url = reverse("park_popularity")
        response = self.client.get(url)

        self.assertEqual(response.data[0]["park_name"], "남산공원")
        self.assertEqual(response.data[1]["park_name"], "서울대공원")
        self.assertEqual(response.data[2]["park_name"], "간데메공원")
        
        
# 토글 공원 리스트 테스트
class ToggleParkListTest(APITestCase):
    def create_park(self, park_data):        
        self.park = ParkModel.objects.create(**park_data)

        self.park.save()

    @classmethod
    def setUpTestData(cls):        
        park_data_1 = {
            "park_name": "서울대공원",
            "zone": "과천시",
            "addr_dong": "ㄱ",
            "image": "1",
            "check_count": "5"
        }
        
        park_data_2 = {
            "park_name": "남산공원",
            "zone": "중구",
            "addr_dong": "ㅈ",
            "image": "2",
            "check_count": "10"
        }
        
        park_data_3 = {
            "park_name": "간데메공원",
            "zone": "동대문구",
            "addr_dong": "ㄷ",
            "image": "3",
            "check_count": "1"
        }
        
        park_data_4 = {
            "park_name": "효창공원",
            "zone": "용산구",
            "addr_dong": "ㅇ",
            "image": "4",
            "check_count": "0"
        }

        cls.create_park(cls, park_data_1)
        cls.create_park(cls, park_data_2)
        cls.create_park(cls, park_data_3)
        cls.create_park(cls, park_data_4)
                
    def test_get_toggle_list(self):
        url = reverse("toggle_park")
        response = self.client.post(url,{"data": "ㄱ"})
        response_2 = self.client.post(url,{"data": "ㅈ"})
        response_3 = self.client.post(url,{"data": "ㄷ"})
        response_4 = self.client.post(url,{"data": "ㅇ"})
        
        self.assertEqual(response.data[0]["park_name"], "서울대공원")
        self.assertEqual(response_2.data[0]["park_name"], "남산공원")
        self.assertEqual(response_3.data[0]["park_name"], "간데메공원")
        self.assertEqual(response_4.data[0]["park_name"], "효창공원")
        
