from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth.models import User
from .models import Category, Exercise, ExerciseItem, Rating, Subscription, SubscriptionItem, Trainee, Trainer,User


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
        fields = ["id","username", "password", "first_name", "last_name", "refresh", "access"]

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
        fields = ["id",'first_name', 'last_name', 'username']

class TraineeDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Trainee
        fields = "__all__"
    def update(self, instance, validated_data):
        user = User.objects.get(id=instance.user.id)
        user.first_name= self.context['request'].data['first_name']
        user.last_name= self.context['request'].data['last_name']
        user.save()
        return super().update(instance, validated_data)

class TrainerListSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    rating=serializers.SerializerMethodField()
    class Meta:
        model = Trainer
        fields = ['user','age', 'experience', 'specialty',"image","rating" ]

    def get_rating(self, obj):
        ratings = Rating.objects.filter(trainer=obj)
        rating = 0.0
        rating_obj = 0.0
        for rate in ratings:
            rating=rating+rate.rating
        if len(ratings)>0:
            rating_obj = rating/len(ratings)
        return round(rating_obj,2)
        
class TrainerSubscriptionListSerializer(serializers.ModelSerializer):
    trainer_name = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = Subscription
        fields = ["id",'name', 'price', 'description', 'trainer','duration',"trainer_name",]

    def get_trainer_name(self, obj):
        return str(obj.get_trainer_name())
    def get_id(self, obj):
        return obj.trainer.user.id
    
class TrainerDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    id = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    subscription = serializers.SerializerMethodField()


    class Meta:
        model = Trainer
        fields = ["id",'user', 'age', 'experience', 'specialty',"image","subscription","rating"]

    def get_rating(self, obj):
        ratings = Rating.objects.filter(trainer=obj)
        rating = 0.0
        rating_obj = 0.0
        for rate in ratings:
            rating=rating+rate.rating
        if len(ratings)>0:
            rating_obj = rating/len(ratings)
        return round(rating_obj,2)

    def get_id(self, obj):
            return obj.user.id
    def get_subscription(self,obj):
        try:
            plan = Subscription.objects.get(trainer = obj)
            plan_obj = TrainerSubscriptionListSerializer(plan).data
        except:
            plan_obj = None
        return plan_obj
        
        
class ExerciseSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    trainer= TrainerDetailSerializer()
    class Meta:
        model= Exercise
        fields = ["id","name","short_description","image","video","category_name","trainer"]

    def get_category_name(self, obj):
        return str(obj.get_category())

class ExerciseItemSerializer(serializers.ModelSerializer):
    exercise= ExerciseSerializer()
    time= serializers.SerializerMethodField()
    class Meta:
        model= ExerciseItem
        fields = ['id','trainee', 'exercise', 'reps', 'sets', 'time', 'done',"date"]
    
    def get_time(self,obj):
        return str(obj.get_time())
class SubscribeSerilizer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    trainer = serializers.SerializerMethodField()

    class Meta:
        model= SubscriptionItem
        fields = ["id","start_date","end_date","active","payment_status","auto_renew","plan","trainee","trainer","price"]
    def get_trainer(self,obj):
        return str(obj.get_trainer())
    def get_price(self,obj):
        return str(obj.get_price())

class CategorySerilizer(serializers.ModelSerializer):
    class Meta:
        model= Category
        fields = "__all__"

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Rating
        fields = "__all__"