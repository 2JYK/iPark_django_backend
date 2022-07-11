from django.db import models


class Option(models.Model):
    option_name = models.CharField("공원 옵션", max_length=50)

    def __str__(self):
        return self.option_name


class Park(models.Model):
    option = models.ManyToManyField(Option, verbose_name="공원 옵션", related_name="options")
    p_park = models.CharField("공원명", max_length=200)
    p_addr = models.CharField("공원주소", max_length=200)
    p_zone = models.CharField("지역", max_length=100)
    p_admintel = models.CharField("전화번호", max_length=20)
    main_equip = models.TextField("주요시설")
    template_url = models.URLField("바로가기", max_length=200)
    p_list_content = models.TextField("공원개요")
    p_img = models.CharField("이미지", max_length=300)
    longitude = models.CharField("X좌표", max_length=50)
    latitude = models.CharField("Y좌표", max_length=50)
    created_at = models.DateTimeField("공원 정보 생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("공원 정보 수정시간", auto_now=True)

    def __str__(self):
        return self.p_park


class ParkComment(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    park = models.ForeignKey(Park, verbose_name="공원", on_delete=models.CASCADE)
    comments = models.TextField("댓글")
    created_at = models.DateTimeField("공원 댓글 생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("공원 댓글 수정시간", auto_now=True)

    def __str__(self):
        return f'{self.user} -> {self.comments}'