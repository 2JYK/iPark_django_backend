from rest_framework import serializers

from user.models import User as UserModel


EMAIL = ("@naver.com", "@gmail.com", "@kakao.com")


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserModel
        fields = ["username", "password", "fullname", "email", "phone", "birthday", "region", "join_date"]
        
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def validate(self, data):
        if data.get("username"):
            if not len(data.get("username", "")) >= 6:
                raise serializers.ValidationError(
                    detail={"error": "username의 길이는 6자리 이상이어야 합니다."}
                )
                
        if not data.get("email", "").endswith(EMAIL):
            raise serializers.ValidationError(
                detail={"error": "네이버, 구글, 카카오 이메일만 가입할 수 있습니다."}
            )
            
        if not len(data.get("password", "")) >= 6:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 6자리 이상이어야 합니다."}
            )
            
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
    