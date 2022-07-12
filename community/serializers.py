from rest_framework import serializers
from community.models import Article as ArticleModle


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModle
        fields = ["id", "user", "tag", "image", "title", "content",
                  "check_count","created_at", "updated_at"]