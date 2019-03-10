from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Message, Friend, Like
from .forms import PostForm
from django.views import generic
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import sys, os, pickle
from .imagenet import imagenet
from .recommend_user import recommend_user, users_to_array, get_users

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
        msg              = Message()
        msg.owner        = request.user
        msg.photo        = request.FILES['photo']
        # vggで稀に発生するエラーが発生した場合にメッセージを投げる
        try:
            imagenet_results = imagenet(msg.photo)
            msg.img_subject  = imagenet_results[0][1]
            msg.img_acc      = imagenet_results[0][2]
            msg.content      = request.POST['content']
            msg.save()
            # 推論結果の情報のDictを作成
            results_dic = {obj:pred for ctg,obj,pred in imagenet_results}

            user_pkl_filepath = 'pickles/%s.pkl' %(msg.owner)
            # ファイルが存在する場合
            if os.path.isfile(user_pkl_filepath):
                # 現存ファイルを読み込み、Dictを書き換える
                with open(user_pkl_filepath, 'rb') as f:
                    user_results = pickle.load(f)
                    # 現存dictのkeysで重複するカラムがあった場合に値を足し、存在しない場合は新規追加する
                    for obj,pred in results_dic.items():
                        if obj in user_results.keys():
                            user_results[obj] += pred
                        else:
                            user_results[obj] = pred
                # ファイル保存
                with open(user_pkl_filepath, 'wb') as f:
                    pickle.dump(user_results, f)

            # 初投稿の場合 pklファイルを新規作成する
            else:
                with open(user_pkl_filepath, 'wb') as f:
                    pickle.dump(results_dic, f)

            return redirect(to='/app')

        #TODO 結局エラーメッセージが画面に出力される。画面を遷移させるには新しいviewを作らないと(実装未定)(もしくはリダイレクトさせたい)
        except TypeError:
            messages.success(request, 'Sorry, something to wrong. Try again...')

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
    is_like  = Like.objects.filter(owner=request.user).filter(message=like_msg).count()
    # いいね済みかどうかを判定させる
    if is_like > 0:
        messages.success(request, 'You were already liked.')
        return redirect(to='/app')

    # いいねカウント
    like_msg.like_count += 1
    like_msg.save()
    # いいねを作成
    like         = Like()
    like.owner   = request.user
    like.message = like_msg
    like.save()
    messages.success(request, 'Liked!')

    return redirect(to='/app')

@login_required(login_url='/admin/login/')
def recommend(request):
    # 類似度が近しいユーザの3人のDict
    arrows = []
    for user in get_users():
        results = recommend_user(user)
        # 投稿がない場合はNoneが返ってくる
        if results is None:
            continue
        for result in results.items():
            # vueに都合のいい配列の形に整形
            arrows.append({'from': result[0].id, 'to': result[1][1].id, 'arrows':'to'})
    users_array = users_to_array(request.user)
    params = {
            'login_user'  : request.user,
            'users_array' : users_array,
            'arrows'      : arrows,
            'results'     : recommend_user(request.user)
            }

    return  render(request, 'app/recommend.html', params)

@login_required(login_url='/admin/login/')
def user_detail(request,id):
    # 全投稿情報を取得
    user_contents = Message.objects.all()
    # 全ユーザオブジェクトを取得
    user          = User.objects.get(id=id)
    params = {
            'login_user' : request.user,
            'user'       : user,
            'contents'   : user_contents,
            }

    return render(request, 'app/user_detail.html', params)
