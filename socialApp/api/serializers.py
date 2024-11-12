
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from ..models import Lesson, UserProfile, TakenLesson, Friendship
from django.contrib.auth.models import User

# Convert your models to JSON

class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Fields you want to include

class UserProfileSerializer(serializers.ModelSerializer):
    # We use the UserSerializer to get the full details of the user
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'followers', 'following']  # We include the necessary fields

class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user']

class FriendshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friendship
        fields = "__all__"

class TakenLessonSerializer(ModelSerializer):
    class Meta:
        model = TakenLesson
        fields = "__all__"

class UserLessonSerializer(serializers.ModelSerializer):
    # TakenLesson has a ForeignKey relationship to Lesson
    # Include the complete details of the lesson within the UserLessonSerializer serializer
    lesson = LessonSerializer()

    class Meta:
        model = TakenLesson
        fields = ['lesson']

class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(required=True,validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True}  # So that the password is not included in the responses
        }

    def create(self, validated_data):
        # Create a new user using the create_user method, which handles password encryption
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user