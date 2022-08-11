from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class iParkTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # 로그인한 사용자의 클레임 설정하기.
        token['id'] = user.id
        token['username'] = user.username

        return token