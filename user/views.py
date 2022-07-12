from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
import re

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
    
    
class FindUserInfoView(APIView):
    # 아이디 찾기
    def post(self, request):
        correct_email = re.compile('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
        correct_phone = re.compile('\d{3}-\d{4}-\d{4}')
        
        email_input = correct_email.match(request.data["email"])
        phone_input = correct_phone.match(request.data["phone"])
        
        if email_input == None or phone_input == None:
            return Response({'msg': '이메일 혹은 핸드폰 번호 양식이 올바르지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            searched_username = UserModel.objects.get(Q(email=request.data["email"]) & Q(phone=request.data["phone"])).username
        
        if searched_username:
            return Response({"username" : searched_username}, status=status.HTTP_200_OK)
        
