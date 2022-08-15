from django.db import models


class Option(models.Model):
    option_name = models.CharField("공원 옵션", max_length=50)

    def __str__(self):
        return self.option_name


class Park(models.Model):
    option = models.ManyToManyField(Option, verbose_name="공원 옵션", related_name="options", through="ParkOption")
    park_name = models.CharField("공원명", max_length=200)
    addr = models.CharField("공원주소", max_length=200)
    zone = models.CharField("지역", max_length=100)
    addr_dong = models.CharField("동", max_length=100)
    admintel = models.CharField("전화번호", max_length=100)
    main_equip = models.TextField("주요시설", blank=True)
    template_url = models.URLField("바로가기", max_length=200, blank=True)
    list_content = models.TextField("공원개요")
    image = models.CharField("이미지", max_length=300)
    longitude = models.CharField("X좌표", max_length=50, blank=True)
    latitude = models.CharField("Y좌표", max_length=50, blank=True)
    check_count = models.PositiveIntegerField("조회수", default=0)
    created_at = models.DateField("공원 정보 생성시간", auto_now_add=True)
    updated_at = models.DateField("공원 정보 수정시간", auto_now=True)

    def __str__(self):
        return self.park_name
    
    @property
    def update_counter(self):
        self.check_count = self.check_count + 1
        self.save()


class ParkOption(models.Model):
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    
    class Meta:
        db_table = "park_park_option"


class ParkComment(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    park = models.ForeignKey(Park, verbose_name="공원", on_delete=models.CASCADE)
    comment = models.TextField("댓글")
    created_at = models.DateTimeField("공원 댓글 생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("공원 댓글 수정시간", auto_now=True)

    def __str__(self):
        return f"{self.user} -> {self.comment}"

class BookMark(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    park = models.ForeignKey(Park, on_delete=models.CASCADE)
    

    class Meta:
        db_table = "park_bookmark"
