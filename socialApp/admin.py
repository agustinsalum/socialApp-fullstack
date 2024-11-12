from django.contrib import admin

from socialApp.models import Lesson, UserProfile, TakenLesson, Friendship

# Register your models here.

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass

@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    pass

@admin.register(TakenLesson)
class LessonAdmin(admin.ModelAdmin):
    pass
