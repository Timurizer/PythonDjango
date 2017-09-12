# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.utils import timezone
from django.contrib.auth.models import User

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

'''
 Тут описаны основные модели, а именно категории заметок, заметки и отношение "любимости"
 Для пользователей используется система, предоставленная с Django
'''


@python_2_unicode_compatible
class Category(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


@python_2_unicode_compatible
class Note(models.Model):
    note_header = models.CharField(max_length=30)
    note_body = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.note_header

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Favourite(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    note_id = models.ForeignKey(Note, on_delete=models.CASCADE)
