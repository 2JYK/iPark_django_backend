from rest_framework import serializers
from park.models import Option as OptionModel
from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel


class OptionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = OptionModel
        fields = ["option_name"]
    

class ParkDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkModel
        fields = [
            "p_park",
            "p_addr",
            "p_admintel",
            "main_equip",
            "template_url",
            "p_list_content",
            "p_img",
            "longitude",
            "latitude",
            "updated_at"
            ]
    

class ParkCommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ParkCommentModel
        fields = [
            "user",
            "park",
            "comments",
            "created_at",
            "updated_at"
            ]