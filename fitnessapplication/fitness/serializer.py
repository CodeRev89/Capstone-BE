from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
from .models import Exercise, ExerciseItem, Subscription, SubscriptionItem, Trainee, Trainer,User


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
        new_user = User(**validated_data)
        new_user.set_password(new_user.password)
        new_user.save()
        token = UserTokenSerializer.get_token(new_user)
        validated_data['refresh'] = str(token)
        validated_data['access'] = str(token.access_token)

    
        return validated_data


class TraineeLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(allow_blank=True, read_only=True)
    
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
        
        payload = RefreshToken.for_user(user_obj)
        token = str(payload.access_token)

        data["access"] = token
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class TrainerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = ['user','age', 'experience', 'specialty',"image" ]
        
  
    
class TrainerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainer
        fields = ['user', 'age', 'experience', 'specialty',"image"]
        
class TrainerSubscriptionListSerializer(serializers.ModelSerializer):
    trainer_name = serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        fields = ['name', 'price', 'describtion', 'trainer','duration',"trainer_name"]

    def get_trainer_name(self, obj):
        return str(obj.get_trainer_name())
        
class ExerciseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()

    class Meta:
        model= Exercise
        fields = ["name","short_description","image","video","category_name"]
    def get_category_name(self, obj):
        return str(obj.get_category())

class ExerciseItemSerializer(serializers.ModelSerializer):
    exercise= ExerciseSerializer()
    class Meta:
        model= ExerciseItem
        fields = ['trainee', 'exercise', 'reps', 'sets', 'time', 'done',"date"]

class SubscribeSerilizer(serializers.ModelSerializer):
    class Meta:
        model= SubscriptionItem
        fields = "__all__"