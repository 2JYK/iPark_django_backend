from django.contrib import admin
from community.models import Tag as TagModel
from community.models import Article as ArticleModel
from community.models import ArticleComment as ArticleCommentModel


admin.site.register(TagModel)
admin.site.register(ArticleModel)
admin.site.register(ArticleCommentModel)