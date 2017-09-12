# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

'''
    для удобство даем админу право управлять всем
    суперюзер логин: admin
    пароль: 123qweasd
    однако все пользователи, созданные с помощью регистрации непосредственно на сайте,
    могут создавать заметки
'''

admin.site.unregister(User)
admin.site.register(Category)
admin.site.register(Note)
admin.site.register(Favourite)
admin.site.register(User)
