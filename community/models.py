from django.db import models


TAG_CHOICES = [
    ('community', '커뮤니티'),
    ('market', '나눔마켓'),
]


class Tag(models.Model):
    tag_name = models.CharField("태그", max_length=10, choices=TAG_CHOICES, default='community')
    
    def __str__(self):
        return self.tag_name


class Article(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, verbose_name="태그", on_delete=models.CASCADE)
    image = models.ImageField("이미지")
    title = models.CharField("제목", max_length=100)
    content = models.TextField("내용")
    created_at = models.DateTimeField("커뮤니티 등록 일자", auto_now_add=True)
    updated_at = models.DateTimeField("커뮤니티 수정 일자", auto_now=True)

    def __str__(self):
        return f'id [ {self.id} ] {self.user.username} 님이 작성한 Article'


class ArticleComment(models.Model):
    user = models.ForeignKey("user.User", verbose_name="작성자", on_delete=models.CASCADE)
    article = models.ForeignKey(Article, verbose_name="게시글", on_delete=models.CASCADE)
    comments = models.TextField("댓글")
    created_at = models.DateTimeField("커뮤니티 댓글 생성시간", auto_now_add=True)
    updated_at = models.DateTimeField("커뮤니티 댓글 수정시간", auto_now=True)

    def __str__(self):
        return f'{self.user} -> {self.comments}'