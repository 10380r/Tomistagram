from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Message, Friend, Like
from .forms import FriendsForm, PostForm

from django.db.models import Q
from django.contrib.auth.decorators import login_required
import sys, os

# indexのビュー関数
@login_required(login_url='/admin/login/')
def index(request):
    # POST時
    if request.method == 'POST':
        file = request.FILES['file']
        path = os.path.join(UPLOADE_DIR, file.name)
        destination = open(path, 'wb')
        for chunk in file.chunks():
            destination.write(chunk)
        insert_data = FileNameModel(file_name = file.name)
        insert_data.save()

        #フォームの用意
        searchform = SearchForm()
        # groupのリストを取得
        gps = Group.objects.filter(owner=request.user)
        glist = [public_group]
        for item in gps:
            glist.append(item)
        # メッセージの取得
        messages = get_your_group_message(request.user, glist, None)
    params = {
            'login_user' : request.user,
            'contents'  : messages,
            'check_form' : checkform,
            'search_form':searchform,
            }
    return  render(request, 'app/index.html', params)

@login_required(login_url='/admin/login/')
def post(request):
    # POST時
    if request.method == 'POST':
        # 送信内容取得
        content = request.POST['content']
        msg         = Message(request.FILES)
        msg.owner   = request.user
        msg.photo   = photo
        msg.content = content
        msg.save()
        return redirect(to='/app')

    # GET時
    else:
        form = PostForm(request.user)
        
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

