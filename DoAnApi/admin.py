# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Post, User, UserLikePost, Comment, Image, AuthUser
# Register your models here.

admin.site.register(Post)
admin.site.register(User)
admin.site.register(AuthUser)
admin.site.register(UserLikePost)
admin.site.register(Comment)
admin.site.register(Image)