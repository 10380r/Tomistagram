import numpy as np
import pickle,django,os,sys
 # ローカルでmodelを扱えるようにする
 # TODO: 任意のパスにするようにできないものか
sys.path.append('/Users/tommy/src/develop/mimicstagram/mimicstagram/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mimicstagram.settings')  # 自分のsettings.py
django.setup()
from app.models import User

def get_pkl(user):
    '''
    引数で渡されたユーザのpklを呼び出す
    '''
    with open('pickles/%s.pkl' %(user), 'rb') as f:
        return pickle.load(f)

def sim_cos(user1, user2):
    '''
    コサイン類似度を計算する
    '''
    cos = np.dot(user1, user2.T) / (np.linalg.norm(user1) * np.linalg.norm(user2))
    return cos

def get_users():
    '''
    全ユーザのリストを作成する
    '''
    users = [user for user in User.objects.all()]
    return users 

def recommend_user(me):
    '''
    全ユーザのコサイン類似度を算出し、レコメンドするユーザの配列を作成する
    '''
    # 一度も投稿したことがないユーザのハンドリング
    try:
        my_dict = get_pkl(me)
    except FileNotFoundError:
        return None

    # 自身のplkを呼び出す
    my_array      = np.fromiter(my_dict.values(), dtype=float)
    users         = get_users()
    recommend_users = []
    # 類似しているユーザーを辞書にする
    for user in users:
        # 自身の場合スキップ
        if user == me:
            continue
        else:
            try:
                # ユーザのpklを呼び出す
                user_dict  = get_pkl(user)
                # 投稿したことがないユーザをフィルタリングして配列を作成
                user_array = np.fromiter(user_dict.values(), dtype=float)
                similarity = sim_cos(my_array, user_array)
                user_tuple = (user,similarity)
                # 先頭3人をトップ３と仮に置く
                if len(recommend_users) < 3:
                    recommend_users.append(user_tuple)
                    print('ADDED => ', recommend_users, '\n')
                # 3位と比較して大きいようならDictに追加
                else:
                    if recommend_users[2][1] < similarity:
                        recommend_users.append(user_tuple)
                # 類似度でソート
                recommend_users = sorted(recommend_users, key=lambda x:x[1], reverse=True)
                # デバッグ用の出力
                print('SORTED =>', recommend_users, '\n')
            # 投稿したことがないユーザの場合の例外処理
            except FileNotFoundError:
                print('"' + str(user) + '"', 'HAS NOT POSTED YET', '\n')
                continue

    # 類似度が高いユーザの配列を作成。Vue.jsに渡すarray
    #arrows = [{'from': user.id, 'to': me.id, 'arrows':'to'} for user,sim in recommend_users[:3]]
    results = {user:[sim, me] for user,sim in recommend_users[:3]}
    return results

def users_to_array(me):
    '''
    Vue.jsに対応した全ユーザの配列を作成する
    '''
    # 類似しているユーザーを辞書にする
    # TODO: vueで表示されるユーザネームをリンクテキストにしたい
    # '<a href="user_detail/%s">%s</a>' %(user.id, str(user))
    users  = [{'id': user.id, 'label': str(user), 'mass': 2} for user in get_users()]
    for user in users:
        # 自身の場合にユーザネームをMeに置換。スケールする
        if user['id'] == me.id:
            user['label'] = 'You'
            user['value'] = 40
            user['scaling'] = {'label': {'enabled': 'true'}}
    return users
