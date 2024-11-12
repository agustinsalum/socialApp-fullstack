from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save

# Create your models here.

class Lesson(models.Model):
    name = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # User -> you
    followers = models.ManyToManyField('self', symmetrical=False, related_name='Usersfollowers', blank=True)
    # you -> User
    following = models.ManyToManyField('self', symmetrical=False, related_name='Usersfollowing', blank=True)


    def __str__(self):
        return self.user.username
    
    """ signals!!Methods that creates an instance in UserProfile when a user is created. Either by registration or google """
    
    # Method that connects to the "post_save" signal of the User model and creates an instance of UserProfile associated with the newly created user.

    @classmethod
    def create_user_profile(cls, sender, instance, created, **kwargs):
        if created:
            cls.objects.create(user=instance)
    
    # Method connected to the same signal that ensures that the UserProfile instance is saved whenever the User model is saved.

    @classmethod
    def save_user_profile(cls, sender, instance, **kwargs):
        instance.userprofile.save()

post_save.connect(UserProfile.create_user_profile, sender=User)
post_save.connect(UserProfile.save_user_profile, sender=User)

class Friendship(models.Model):
    from_user = models.ForeignKey(UserProfile, related_name='friendship_creator', on_delete=models.CASCADE)
    to_user = models.ForeignKey(UserProfile, related_name='friendship_receiver', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.user.username} follows {self.to_user.user.username}"
    
    # when a new Friendship instance is created, the save() method is called after the relationship is saved
    def save(self, *args, **kwargs):
        # Check if Friendship is a new instance
        is_new = self.pk is None
        super(Friendship, self).save(*args, **kwargs)
        
        # Update followers and following
        if is_new:
            self.from_user.following.add(self.to_user) 
            self.to_user.followers.add(self.from_user)



class TakenLesson(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    times_taken = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'lesson')
    
    def __str__(self):
        return f"{self.user.user.username} - {self.lesson.name}"

