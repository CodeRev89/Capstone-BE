from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from .models import Trainee


class UserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class TraineeRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "first_name", "last_name", "refresh", "access"]

    def create(self, validated_data):
        username = validated_data["username"]
        password = validated_data["password"]
        new_user = User(username=username)
        new_user.set_password(new_user.password)
        new_user.save()
        token = UserTokenSerializer.get_token(new_user)
        validated_data['refresh'] = str(token)
        validated_data['access'] = str(token.access_token)
        return validated_data


class TraineeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        my_username = data.get("username")
        my_password = data.get("password")

        try:
            user_obj = User.objects.get(username=my_username)
        except User.DoesNotExist:
            raise serializers.ValidationError("This username does not exist")

        if not user_obj.check_password(my_password):
            raise serializers.ValidationError(
                "Incorrect username/password combination!")

        return data
