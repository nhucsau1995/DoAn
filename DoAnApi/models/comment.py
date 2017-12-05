from django.db import models
from .userpj import User
from .post import Post

class Comment(models.Model):
    objects = models.Manager()

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    content = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return '{}/{} - {}'.format(self.id, self.post_id.title, self.user_id.id)

