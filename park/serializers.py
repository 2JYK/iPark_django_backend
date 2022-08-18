from rest_framework import serializers

from park.models import Option as OptionModel
from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel
from park.models import BookMark as BookMarkModel


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionModel
        fields = ["option_name"]
    

class ParkCommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return obj.user.username
    
    class Meta:
        model = ParkCommentModel
        fields = ["user", "park", "comment", "updated_at", "id", "user_id"]


class ParkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkModel
        fields = ["id", "park_name","image", "check_count"]


class BookMarkSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMarkModel
        fields = ["id","park", "user"]


class ParkDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkModel
        fields = ["id", "park_name", "addr", "image", "list_content", "admintel",
                  "longitude", "latitude", "main_equip", "template_url", "updated_at",
                  "check_count"]
    

class ToggleParkListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkModel
        fields = ["id", "park_name"]
