from rest_framework import serializers

from park.models import Option as OptionModel
from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel


class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = OptionModel
        fields = ["option_name"]
    

class ParkCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkCommentModel
        fields = ["user", "park", "comment"]
        
        
class ParkDetailSerializer(serializers.ModelSerializer):
    comments = ParkCommentSerializer(many=True, read_only=True, source="parkcomment_set")

    class Meta:
        model = ParkModel
        fields = ["p_park", "p_addr", "p_img", "p_list_content", "p_admintel",
                  "longitude", "latitude", "main_equip", "template_url", "updated_at",
                  "comments"]
    
