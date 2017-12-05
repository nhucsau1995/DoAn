from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from .userpj import User

class Post(models.Model):
    CHOICES = (
        (0, 'All'),
        (1, 'male'),
        (2, 'female'),
    )

    objects = models.Manager()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    type = models.CharField(max_length=254, null=False, blank=False)
    title = models.CharField(max_length=254, null=False, blank=False)
    customer = models.PositiveSmallIntegerField(choices=CHOICES, null=True, blank=True)
    price = models.FloatField(null=False, blank=False)
    area = models.FloatField(null=False, blank=False)
    province = models.CharField(max_length=140, null=False, blank=False)
    district = models.CharField(max_length=140, null=False, blank=False)
    address = models.CharField(max_length=500, null=False, blank=False)
    video = models.FileField(blank=False, null=False, upload_to='video')
    description = models.TextField(blank=False, null=False)
    like_number = models.IntegerField(null=False, blank=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True, auto_now=False, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    def __str__(self):
        return '{}'.format(self.title)


def create_slug(instance):
    if not instance.slug:
        slug = slugify(instance.title)
        ori_slug = slug
        counter = 1
        while True:
            qs = Post.objects.filter(slug=slug)
            exists = qs.exists()
            if not exists:
                return slug
            slug = "%s-%s" %(ori_slug, counter)
            counter += 1
    return False



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)