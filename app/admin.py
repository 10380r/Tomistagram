from django.contrib import admin
from .models import Message, Friend, Like

admin.site.register(Message)
admin.site.register(Friend)
admin.site.register(Like)
