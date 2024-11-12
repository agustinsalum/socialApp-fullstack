from rest_framework import routers
from .viewsets import LessonViewSet, UserProfileViewSet, TakenLessonViewSet, FriendshipViewSet

# Automatically generate routes based on the ViewSet,

router = routers.SimpleRouter()

# In this case it is appended to the route of the app's urls
router.register("lessons",LessonViewSet)
router.register("usersProfile",UserProfileViewSet)
router.register("takenLessons",TakenLessonViewSet)
router.register("friendships", FriendshipViewSet)
