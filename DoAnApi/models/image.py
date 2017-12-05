from django.db import models

from .post import Post

class Image(models.Model):
    objects = models.Manager()

    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)

    image = models.ImageField(blank=False, null=False, upload_to='image')

    def __str__(self):
        return '{}/{}'.format(self.id, self.post_id.title)


