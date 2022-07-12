from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer

from user.models import User as UserModel


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    
    # 회원가입
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    def put(self, request):
        user = UserModel.objects.get(id=request.user.id)
        
        serializer = UserSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원탈퇴
    def delete(self, request):
        user = request.user
        
        if user:
            user.delete()
            return Response({"message": "회원탈퇴 성공"}, status=status.HTTP_200_OK)
        
        return Response({"message": "회원탈퇴 실패"}, status=status.HTTP_400_BAD_REQUEST)
    
    