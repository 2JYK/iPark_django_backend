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

    