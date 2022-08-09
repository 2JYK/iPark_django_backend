from django.contrib.auth.hashers import check_password
from django.db.models import Q
import re
from rest_framework import serializers

from user.models import User as UserModel


EMAIL = ("@naver.com", "@gmail.com", "@kakao.com", "@daum.net", "@nate.com", "@outlook.com")


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email", "phone", "region", "join_date"]
        
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def validate(self, data):
        correct_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        password_input = correct_password.match(data.get("password", ""))
        
        if data.get("username"):
            try:
                if UserModel.objects.get(username=data.get("username")):
                    raise serializers.ValidationError(
                        detail={"username": "이미 존재하는 username입니다."}
                    )
            except:
                if not len(data.get("username", "")) >= 6:
                    raise serializers.ValidationError(
                    detail={"username": "username의 길이는 6자리 이상이어야 합니다."})
        
        if password_input == None:
            raise serializers.ValidationError(
                detail={"password": "비밀번호는 8 자리 이상이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."})
        
        return data
        
    def create(self, validated_data):
        password = validated_data.pop("password", "")
        
        user = UserModel(**validated_data)
        user.set_password(password)
        user.save()
        
        return user
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()
        
        return instance
    
    
class AccountUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email",
                  "phone", "region", "join_date"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        correct_password = re.compile("^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$")
        
        if data.get("password"):
            password_input = correct_password.match(data.get("password"))
            
            if password_input == None:
                raise serializers.ValidationError(
                detail={"password": "비밀번호는 8 자리 이상이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."})
        
        if data.get("username"):
            try:
                if UserModel.objects.get(username=data.get("username")):
                    raise serializers.ValidationError(
                        detail={"username": "이미 존재하는 username입니다."}
                    )
            except:
                if not len(data.get("username", "")) >= 6:
                    raise serializers.ValidationError(
                    detail={"username": "username의 길이는 6자리 이상이어야 합니다."})
                    
        return data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                user = UserModel.objects.get(Q(username=validated_data["username"]) & Q(email=validated_data["email"]))
                if check_password(value, user.password):
                    raise serializers.ValidationError(
                        detail={"password": "현재 사용중인 비밀번호와 동일한 비밀번호는 입력할 수 없습니다."})
                else:
                    instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        return instance
