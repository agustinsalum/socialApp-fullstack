
from django.urls import path
from .router import router
from .viewsets import (
    UserProfileViewSet,
    TakenLessonViewSet,
    RandomDogImageView,
    HttpCatImageView,
    WeatherView,
    LogoutView,
    HomeView,
    RegisterUserView
)

from rest_framework_simplejwt import views as jwt_views

# Define the URLs to access the views. In our case with the help of the router that does them automatically.

app_name = "socialApp"

urlpatterns = [
    path('usersProfile/<int:pk>/friends/', UserProfileViewSet.as_view({'get': 'friends'}), name='user-friends'),
    path('usersProfile/<int:pk>/friends_lessons/', UserProfileViewSet.as_view({'get': 'friends_lessons'}), name='friends-lessons'),
    path('usersProfile/non-staff-users/', UserProfileViewSet.as_view({'get': 'non_staff_users'}), name='non-staff-users'),
    path('takenLessons/<int:pk>/user_lessons/', TakenLessonViewSet.as_view({'get': 'user_lessons'}), name='user-lessons'),
    path('random-dog/', RandomDogImageView.as_view(), name='random-dog'),
    path('http-cat/<int:status_code>/', HttpCatImageView.as_view(), name='http-cat'),
    path('weather/<str:city_name>/', WeatherView.as_view(), name='weather'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('home/', HomeView.as_view(), name='home'),
    path('register/', RegisterUserView.as_view(), name='register')
]

urlpatterns += router.urls