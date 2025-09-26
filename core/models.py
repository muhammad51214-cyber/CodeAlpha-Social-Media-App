from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=160, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile({self.user.username})"

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post({self.id}) by {self.author.username}"

    @property
    def like_count(self):
        return self.likes.count()

class Comment(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Comment({self.id}) on Post({self.post_id})"

class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "post"], name="unique_like_user_post"),
        ]

    def __str__(self):
        return f"Like(user={self.user_id}, post={self.post_id})"

class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["follower", "following"], name="unique_follow_pair"),
        ]

    def __str__(self):
        return f"{self.follower.username} -> {self.following.username}"

    @staticmethod
    def following_ids_for(user: User):
        return Follow.objects.filter(follower=user).values_list("following_id", flat=True)