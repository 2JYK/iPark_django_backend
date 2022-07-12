from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from park.models import Park as ParkModel

from park.serializers import ParkDetailSerializer


class ParkView(APIView):
    # 공원 상세 정보 조회
    def get(self, request, park_id):
        park = ParkModel.objects.get(id=park_id)
        serialized_data = ParkDetailSerializer(park).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)