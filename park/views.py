from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from park.models import Park as ParkModel
from park.models import ParkComment as ParkCommentModel

from park.serializers import ParkDetailSerializer
from park.serializers import ParkCommentSerializer


class ParkView(APIView):
    # 공원 상세 정보 조회
    def get(self, request, park_id):
        park = ParkModel.objects.get(id=park_id)
        serialized_data = ParkDetailSerializer(park).data
        
        return Response(serialized_data, status=status.HTTP_200_OK)
    

# 공원 상세 페이지의 댓글창    
class ParkCommentView(APIView):
    # 댓글 작성
    def post(self, request, park_id):
        if request.user.is_anonymous:
            return Response({"message": "로그인을 해주세요"}, status=status.HTTP_401_UNAUTHORIZED)
        

        park = ParkModel.objects.get(id=park_id)
        
        data = {
            "user" : request.user.id,
            "park" : park.id,
            "comment" : request.data["comment"]
        }
        
        comment_serializer = ParkCommentSerializer(data=data)

        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        
        return Response({"message": "내용을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
    
    # 댓글 수정
    def put(self, request, comment_id):
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
        try:
            comment = ParkCommentModel.objects.get(id=comment_id, user=request.user)
            comment.delete()
            
            return Response({"message": "해당 댓글이 삭제되었습니다"}, status=status.HTTP_200_OK)
        
        except ParkCommentModel.DoesNotExist:
            return Response({"message": "해당 댓글이 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)     