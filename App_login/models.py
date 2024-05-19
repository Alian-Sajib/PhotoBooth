from django.db import models
from django.contrib.auth.models import User

# from App_login.forms import


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile"
    )
    full_name = models.CharField(max_length=264, blank=True)
    description = models.TextField(blank=True)
    profile_pic = models.ImageField(upload_to="profile_pics", blank=True)
    dob = models.DateField(blank=True, null=True)
    facebook = models.URLField(blank=True)
    website = models.URLField(blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follower"
    )
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="following"
    )
    date_created = models.DateTimeField(auto_now_add=True)
