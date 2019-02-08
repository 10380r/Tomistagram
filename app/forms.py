from django import forms
from.models import Message, Friend, Like
from django.contrib.auth.models import User

# Messageフォーム
class MessageFrom(forms.ModelForm):
    class Meta:
        model  = Message
        fields = ['owner', 'content']

# Friendフォーム
class FriendForm(forms.ModelForm):
    class Meta:
        model  = Friend
        fields = ['owner', 'user']

# Likeフォーム
class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['owner', 'message']

class FriendsForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(FriendsForm, self).__init__(*args, **kwargs)
        self.fields['friends'] = forms.MultipleChoiceField(
                choices = [(item.user, item.user) for item in friends],
                widget  = forms.CheckboxSelectMultiple(),
                inital  = vals
                )

class PostForm(forms.Form):
    content = forms.CharField(max_length=150, widget = forms.Textarea)
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='admin').first()
