from django.db import models
from django.db.models import signals

from .userpj import User
from .post import Post

class UserLikePost(models.Model):
    objects = models.Manager()

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return '{}/{} - {}'.format(self.id, self.post_id.id, self.user_id.username)


def increase_like_number(sender, instance, created, raw, **kwargs):
    if created:
        instance.post_id.like_number += 1
        instance.post_id.save()


def decrease_like_number(sender, instance, **kwargs):
    instance.post_id.like_number -= 1

    if instance.post_id.like_number < 0:
        instance.post_id.like_number = 0
    instance.post_id.save()


signals.post_save.connect(increase_like_number, sender=UserLikePost)
signals.post_delete.connect(decrease_like_number, sender=UserLikePost)