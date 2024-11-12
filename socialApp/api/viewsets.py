
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from ..models import Lesson, UserProfile, TakenLesson, Friendship
from .serializers import LessonSerializer, UserProfileSerializer, TakenLessonSerializer, FriendshipSerializer, FriendSerializer, UserLessonSerializer, UserCreateSerializer
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.views import APIView
from .dog_api import get_random_dog_image
from .cat_api import get_http_cat_image
from .weather_api import get_weather
import os
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

# View that uses the serializer to display the data

class LessonViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]


# List all users in the system

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    # List of all friends for a specific user

    @action(detail=True, methods=['get'])
    def friends(self, request, pk=None):
        user_profile = self.get_object()
        friends = user_profile.following.all()
        serializer = FriendSerializer(friends, many=True)
        return Response(serializer.data)
    
    # List of lessons taken by friends of a specific user

    @action(detail=True, methods=['get'])
    def friends_lessons(self, request, pk=None):
        user_profile = self.get_object()
        friends = user_profile.following.all()
        taken_lessons = TakenLesson.objects.filter(user__in=friends)
        serializer = UserLessonSerializer(taken_lessons, many=True)
        return Response(serializer.data)
    
    # List the users who are not staff members
    
    @action(detail=False, methods=['get'], url_path='non-staff-users')
    def non_staff_users(self, request):
        non_staff_users = UserProfile.objects.filter(user__is_staff=False)
        serializer = UserProfileSerializer(non_staff_users, many=True)
        return Response(serializer.data)

# List all friendships registered in the system

class FriendshipViewSet(ModelViewSet):
    queryset = Friendship.objects.all()
    serializer_class = FriendshipSerializer
    permission_classes = [permissions.IsAuthenticated]

class TakenLessonViewSet(ModelViewSet):
    queryset = TakenLesson.objects.all()
    serializer_class = TakenLessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    # List of lessons that a specific user has taken

    @action(detail=True, methods=['get'])
    def user_lessons(self, request, pk=None):
        user_profile = UserProfile.objects.get(pk=pk)
        taken_lessons = TakenLesson.objects.filter(user=user_profile)
        serializer = UserLessonSerializer(taken_lessons, many=True)
        return Response(serializer.data)

# public-apis (dog)

class RandomDogImageView(APIView):
    def get(self, request, *args, **kwargs):
        dog_image_data = get_random_dog_image()
        if dog_image_data.get('status') == 'success':
            return Response(dog_image_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'API error'}, status=status.HTTP_400_BAD_REQUEST)

# public-apis (cat)

class HttpCatImageView(APIView):
    def get(self, request, status_code, *args, **kwargs):
        cat_image_data = get_http_cat_image(status_code)
        if cat_image_data:
            return Response(cat_image_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid status code or API error'}, status=status.HTTP_400_BAD_REQUEST)
        

# private-api

class WeatherView(APIView):
    def get(self, request, city_name, *args, **kwargs):
        api_key = os.getenv('OPENWEATHER_API_KEY', settings.OPENWEATHER_API_KEY)
        weather_data = get_weather(city_name, api_key)
        if weather_data:
            return Response(weather_data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Could not fetch weather data'}, status=status.HTTP_400_BAD_REQUEST)

# logout

from rest_framework_simplejwt.tokens import RefreshToken

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]


class HomeView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        # Get the current user
        user = request.user
        data = {
            "message": f"Hi, {user.username}!"
        }
        return Response(data)