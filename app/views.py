from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Friend, Like
from .forms import FriendsForm, PostForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required
import sys, os
from .imagenet import imagenet

# indexのビュー関数
@login_required(login_url='/admin/login/')
def index(request):
    # POST時
    # メッセージの取得
    messages = Message.objects.all()

    params = {
            'login_user' : request.user,
            'contents'   : messages,
            }
    return  render(request, 'app/index.html', params)

@login_required(login_url='/admin/login/')
def post(request):
    # POST時
    if request.method == 'POST':
        # 送信内容取得
        msg             = Message()
        msg.owner       = request.user
        msg.photo       = request.FILES['photo']
        imagenet_result = imagenet(msg.photo)[0]
        msg.img_subject = imagenet_result[1]
        msg.img_acc     = imagenet_result[2]
        msg.content     = request.POST['content']
        msg.save()
        return redirect(to='/app')
    # GET時
    else:
        form = PostForm()
        
    params = {
            'login_user' : request.user,
            'form'       : form,
            }
    return render(request, 'app/post.html', params)

@login_required(login_url='/admin/login/')
def like(request, like_id):
    # いいねするメッセージを取得
    like_msg = Message.objects.get(id=like_id)
    is_like  = Like.objects.filter(owner=request.user) \
            .filter(message=like_msg).count()
    # いいね済みかどうか
    if is_like > 0:
        messages.success(request, 'you were already liked.')
        return redirect(to='/app')

    # いいねカウント
    like_msg.like_count += 1
    like_msg.save()
    # いいねを作成
    like = Like()
    like.owner = request.user
    like.message = like_msg
    like.save()

    messages.success(request, 'Liked!')
    return redirect(to='/app')
