from rest_framework import serializers

from community.models import Article as ArticleModle
from community.models import ArticleComment as ArticleCommentModel


class ArticleCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    created_at_time = serializers.SerializerMethodField()

    def get_username(self,obj):
        return obj.user.username

    def get_created_at_time(self, obj):
        created_at_time = obj.created_at.replace(microsecond=0).isoformat()
        return created_at_time

    class Meta:
        model = ArticleCommentModel
        fields = ["id", "article", "user", "username", "comment", 
                  "created_at_time", "created_at", "updated_at"]


class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    tag_name = serializers.SerializerMethodField()
    park_name = serializers.SerializerMethodField()
    created_at_time = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    def get_username(self, obj):
        return obj.user.username

    def get_tag_name(self, obj):
        return obj.tag.tag_name
    
    def get_park_name(self, obj):
        return obj.park.park_name
    
    def get_created_at_time(self, obj):
        created_at_time = obj.created_at.replace(microsecond=0).isoformat()
        return created_at_time
    
    def get_comment_count(self, obj):
        return obj.articlecomment_set.count() 
    
    class Meta:
        model = ArticleModle
        fields = ["id", "user", "tag", "park", "username", "tag_name", "park_name", "image", 
                  "title", "content", "check_count", "comment_count", "created_at", "updated_at", "created_at_time"]