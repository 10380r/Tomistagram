from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    owner       = models.ForeignKey(User, on_delete=models.CASCADE, \
                  related_name = 'message_owner')
    content     = models.TextField(max_length=1000)
    photo       = models.ImageField(upload_to='documents/', default='defo')
    like_count  = models.IntegerField(default=0)
    pub_date    = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s (%s)' %(self.content, self.owner)

    class Meta:
        # - にしておくと、新しい順での表示ができるらしい
        ordering = ('-pub_date',)


class Friend(models.Model):
    owner   = models.ForeignKey(User, on_delete=models.CASCADE,\
              related_name='friend_owner')
    user    = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s (%s)' %(self.user, self.group)

class Like(models.Model):
    owner   = models.ForeignKey(User, on_delete=models.CASCADE,\
              related_name='like_owner')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    def __str__(self):
        return 'Like for " %s " !' %(self.message)
