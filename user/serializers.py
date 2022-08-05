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
            if not len(data.get("username", "")) >= 6:
                raise serializers.ValidationError(
                    detail={"error": "username의 길이는 6자리 이상이어야 합니다."})
                
        if not data.get("email", "").endswith(EMAIL):
            raise serializers.ValidationError(
                detail={"error": "네이버, 구글, 카카오, 다음, 네이트, 아웃룩 이메일만 가입할 수 있습니다."})
        
        if password_input == None:
            raise serializers.ValidationError(
                detail={"error": "비밀번호는 8 자리 이상이며 최소 하나 이상의 영문자, 숫자, 특수문자가 필요합니다."})
        
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
                  "phone", "birthday", "region", "join_date"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        correct_phone = re.compile("(010)-\d{4}-\d{4}")

        phone_input = correct_phone.match(data.get("phone", ""))

        if data.get("username"):
            if not len(data.get("username", "")) >= 6:
                raise serializers.ValidationError(
                    detail={"error": "username의 길이는 6자리 이상이어야 합니다."})

        if not data.get("email", "").endswith(EMAIL):
            raise serializers.ValidationError(
                detail={"error": "네이버, 구글, 카카오, 다음, 네이트, 아웃룩 이메일만 가입할 수 있습니다."})

        if phone_input == None:
            raise serializers.ValidationError(
                detail={"error": "전화번호는 010-0000-0000 형식으로 작성해주시기 바랍니다."})

        return data

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        return instance
