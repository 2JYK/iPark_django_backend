from django.urls import reverse
from rest_framework.test import APITestCase

from park.models import Park as ParkModel
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
                                            updated_at = "updated_at"
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

    
    
    
    
      