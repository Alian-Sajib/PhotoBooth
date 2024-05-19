from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post")
    caption = models.CharField(max_length=264)
    image = models.ImageField(upload_to="posts_images")
    date_posted = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date_posted",]

    def __str__(self):
        return "{} : {}".format(self.author, self.caption)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_user")
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.post, self.user)
