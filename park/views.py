from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel

from park.serializers import ParkDetailSerializer
from park.serializers import ParkCommentSerializer
from park.serializers import ParkSerializer
from park.serializers import ToggleParkListSerializer


class ParkView(APIView):
    # 공원 상세 정보 조회
    def get(self, request, park_id):
        park = ParkModel.objects.get(id=park_id)
        park.check_count += 1
        park.save()
        serialized_data = ParkDetailSerializer(park).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    

# 공원 상세 페이지의 댓글창    
class ParkCommentView(APIView):
    # 댓글 조회
    def get(self, request, park_id):
        comment = ParkCommentModel.objects.filter(park_id=park_id)
        serialized_data = ParkCommentSerializer(comment, many=True).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    
    # 댓글 작성
    def post(self, request, park_id):
        if request.user.is_anonymous:
            return Response({"message": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)

        park = ParkModel.objects.get(id=park_id)
        
        data = {
            "park" : park.id,
            "comment" : request.data["comment"]
        }
        
        comment_serializer = ParkCommentSerializer(data=data)

        if comment_serializer.is_valid():
            comment_serializer.save(user=request.user)
            
            park.check_count -= 1
            park.save()
            
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
            
        return Response({"message": "내용을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 수정
    def put(self, request, comment_id):
        if request.user.is_anonymous:
            return Response({"message": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            try: 
                comment = ParkCommentModel.objects.get(id=comment_id, user=request.user)  
                
            except ParkCommentModel.DoesNotExist:
                return Response({"message": "해당 댓글이 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)      
                    
            if comment.comment == request.data["comment"]: 
                return Response({"message": "수정할 내용을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST) 
                
            comment_serializer = ParkCommentSerializer(comment, data=request.data, partial=True)
            
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data, status=status.HTTP_200_OK)
            
            return Response({"message": "내용을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)

    # 댓글 삭제
    def delete(self, request, comment_id):
        if request.user.is_anonymous:
            return Response({"message": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        
        else:
            try:
                comment = ParkCommentModel.objects.get(id=comment_id, user=request.user)
                comment.delete()
                return Response({"message": "해당 댓글이 삭제되었습니다"}, status=status.HTTP_200_OK)
            
            except ParkCommentModel.DoesNotExist:
                return Response({"message": "해당 댓글이 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)     
            
            
# 검색 페이지
class OptionView(APIView):
    def get(self, request):
        param = request.query_params.getlist("param")
        
        option_list = []
        zone_list = []

        for p in param:
            if p in ["조경", "운동", "놀이공원", "역사", "학습테마", "교양", "편익", "주차장"]:
                option_list.append(p)
            else:
                zone_list.append(p)

        if len(option_list) > 0:
            results = ParkModel.objects.filter(option__option_name__in=option_list).distinct()
        elif len(zone_list) > 0:
            results = ParkModel.objects.filter(zone__in=zone_list).distinct()
        elif len(option_list) > 0 and len(zone_list) > 0:
            # results = ParkModel.objects.filter(Q(option__option_name__in=option_list) & Q(zone__in=zone_list)).distinct()
            results = ParkModel.objects.filter(zone__in=zone_list).filter(option__option_name__in=option_list).distinct()
            
        if results.exists():
            serializer = ParkSerializer(results, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"message": "공원을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
    
    
# 공원 인기순 검색
class ParkPopularityView(APIView):
    def get(self, request):
        popular_park = ParkModel.objects.filter(check_count__gte=1).order_by("-check_count")
        popular_serializer = ParkSerializer(popular_park, many=True)
        
        return Response(popular_serializer.data, status=status.HTTP_200_OK)
    

# 토글 공원 리스트
class ToggleParkView(APIView):
    def get(self, request):
        toggle_parks = ParkModel.objects.all()
        
        toggle_serializer = ToggleParkListSerializer(toggle_parks, many=True)
        return Response(toggle_serializer.data, status=status.HTTP_200_OK)
