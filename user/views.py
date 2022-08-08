from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
import re

from user.serializers import UserSerializer
from user.serializers import AccountUpdateSerializer

from user.models import User as UserModel


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    
    # 회원가입
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 회원정보 수정
    def put(self, request):
        user = UserModel.objects.get(id=request.user.id)
        
        serializer = AccountUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({"error": "입력하신 정보를 확인해주세요"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        correct_email = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        correct_phone = re.compile("\d{3}-\d{4}-\d{4}")
        
        email_input = correct_email.match(request.data["email"])
        phone_input = correct_phone.match(request.data["phone"])
        
        if email_input == None or phone_input == None:
            return Response({"message": "이메일 혹은 핸드폰 번호 양식이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                searched_username = UserModel.objects.get(Q(email=request.data["email"]) & Q(phone=request.data["phone"])).username
                if searched_username:
                    return Response({"username" : searched_username}, status=status.HTTP_200_OK)
                
            except UserModel.DoesNotExist:
                return Response({"message": "사용자가 존재하지 않습니다"}, status=status.HTTP_404_NOT_FOUND)
        

class AlterPasswordView(APIView):
    # 비밀번호를 변경할 자격이 있는지 확인
    def post(self, request):
        correct_email = re.compile("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        email_input = correct_email.match(request.data["email"])
        
        if request.data["username"] == "" or request.data["email"] == "":
            return Response({"message": "아이디 또는 이메일 값을 제대로 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if email_input == None:
                print(email_input)
                return Response({"message": "이메일 형식에 맞게 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try: 
                    user = UserModel.objects.get(Q(username=request.data["username"]) & Q(email=request.data["email"]))
                    if user:
                        user_data = UserSerializer(user)
                        return Response(user_data.data, status=status.HTTP_200_OK)
                
                except UserModel.DoesNotExist:
                    return Response({"message": "존재하지 않는 사용자입니다."}, status=status.HTTP_404_NOT_FOUND)
    
    # 비밀번호 변경
    def put(self, request):
        correct_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        
        if request.data["new_password"] == "" or request.data["rewrite_password"] == "":
            return Response({"message": "비밀번호를 제대로 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if request.data["new_password"] == request.data["rewrite_password"]:
                password_input = correct_password.match(request.data["new_password"])
                
                if password_input == None:
                    return Response({"message": "비밀번호를 양식에 맞게 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    user = UserModel.objects.get(Q(username=request.data["username"]) & Q(email=request.data["email"]))
                    if check_password(request.data["new_password"], user.password):
                        return Response({"message": "현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        user.set_password(request.data["new_password"])
                        user.save()
                
                    return Response({"message": "비밀번호 변경이 완료되었습니다! 다시 로그인해주세요."}, status=status.HTTP_201_CREATED)
            
            return Response({"message": "두 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyView(APIView):
    authentication_classes = [JWTAuthentication]

    # 계정관리 페이지 접근 권한 확인
    def post(self, request):
        correct_password = re.compile(
            "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        password_input = correct_password.match(request.data["password"])

        if request.data["username"] == "" or request.data["password"] == "":
            return Response({"message": "아이디 또는 비밀번호 값을 제대로 입력해주세요."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if password_input == None:
                return Response({"message": "비밀번호 형식에 맞게 작성해주세요."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = authenticate(username=request.data["username"], password=request.data["password"])

                if request.user == user:
                    user = UserModel.objects.get(username=request.data["username"])
                    user_data = UserSerializer(user)

                    return Response(user_data.data, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "존재하지 않는 사용자입니다."}, status=status.HTTP_404_NOT_FOUND)


class KakaoLoginView(APIView):
    # 소셜로그인 : 카카오 계정을 통해 iPark 로그인, 회원가입 진행
    def post(self, request):
        access_token = request.data["access_token"]
        email = request.data["email"]
   
        try:
            user = UserModel.objects.get(email=email)

            if user and (user.password == None):
                return Response({"res_code": 1, 
                                 "message": "iPark 서비스 이용을 위해 회원님의 정보가 필요합니다"}, 
                                status=status.HTTP_200_OK)
                
            elif user and (user.password != None):
                refresh = RefreshToken.for_user(user)
                return Response({"res_code": 2, 
                                 "message" : "로그인 성공",
                                 "refresh": str(refresh), 
                                 "access": str(refresh.access_token)
                                 }, status=status.HTTP_200_OK)
        
        except UserModel.DoesNotExist:
            return Response({"res_code": 1, 
                             "message": "iPark 서비스 이용을 위해 회원님의 정보가 필요합니다"}, 
                            status=status.HTTP_200_OK)
