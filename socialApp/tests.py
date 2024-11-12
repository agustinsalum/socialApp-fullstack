from django.test import TestCase
from django.contrib.auth.models import User
from .models import Lesson, UserProfile, Friendship, TakenLesson

# Create your tests here.

"""

To run the test you must type in your console:

python manage.py test socialApp.tests.ModelsTestCase.test_lesson_creation
"""

class ModelsTestCase(TestCase):
    def setUp(self):
        # When creating a user, their corresponding instance in UserProfile is also created.
        self.user_1 = User.objects.create(username='user_1')
        self.user_profile_1 = UserProfile.objects.get(user=self.user_1)
        self.user_2 = User.objects.create(username='user_2')
        self.user_profile_2 = UserProfile.objects.get(user=self.user_2)
        self.lesson = Lesson.objects.create(name='Statistics', topic='Math')
        self.taken_lesson = TakenLesson.objects.create(user=self.user_profile_2, lesson=self.lesson, times_taken=2)
        self.friendship = Friendship.objects.create(from_user=self.user_profile_1, to_user=self.user_profile_2)


    """ checks if the topic property of the lesson matches the expected value """

    def test_lesson_creation(self):
        lesson = Lesson.objects.get(name='Statistics')
        # assertEqual(a, b): Compares if a is equal to b.
        self.assertEqual(lesson.topic, 'Math')

    def test_user_profile_creation(self):
        # assertIsInstance(obj, cls): Checks if the object obj is an instance of the class cls.54
        self.assertIsInstance(self.user_1, User)
        #
        self.assertIsInstance(self.user_profile_1, UserProfile)
        self.assertEqual(list(self.user_profile_1.followers.all()), [])


    def test_taken_lesson_creation(self):
        pass
        self.assertIsInstance(self.taken_lesson, TakenLesson)
        self.assertEqual(self.taken_lesson.user, self.user_profile_2)
        self.assertEqual(self.taken_lesson.lesson, self.lesson)
        self.assertEqual(self.taken_lesson.times_taken, 2)


    def test_friendship_creation(self):
        self.assertIsInstance(self.friendship, Friendship)
        self.assertEqual(self.friendship.from_user, self.user_profile_1)
        self.assertEqual(self.friendship.to_user, self.user_profile_2)


    def test_friendship_updates_followers_and_following(self):
        # Test if followers and following are updated after Friendship creation
        self.assertEqual(self.user_profile_1.followers.count(), 0)
        self.assertEqual(self.user_profile_1.following.count(), 1)
        self.assertEqual(self.user_profile_2.followers.count(), 1)
        self.assertEqual(self.user_profile_2.following.count(), 0)
