from rest_framework import serializers

from park.models import Option as OptionModel
from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel
from user.models import User as UserModel


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
        fields = ["user", "park", "comment", "updated_at", "id"]
        
        
class ParkDetailSerializer(serializers.ModelSerializer):
    comments = ParkCommentSerializer(many=True, read_only=True, source="parkcomment_set")

    class Meta:
        model = ParkModel
        fields = ["id", "park_name", "addr", "image", "list_content", "admintel",
                  "longitude", "latitude", "main_equip", "template_url", "updated_at",
                  "comments", "check_count"]
    

class ParkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkModel
        fields = ["id", "park_name","image", "check_count"]

        
class BookMarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ["bookmarks"]
        

class ToggleParkListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkModel
        fields = ["id", "park_name"]
