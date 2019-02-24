import numpy as np
import pickle,django,os,sys
 # ローカルでmodelを扱えるようにする
sys.path.append('/Users/tommy/src/develop/mimicstagram/mimicstagram/')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mimicstagram.settings')  # 自分のsettings.py
django.setup()
from app.models import User


def get_pkl(user):
    with open('pickles/%s.pkl' %(user), 'rb') as f:
        return pickle.load(f)

def sim_cos(user1, user2):
    cos = np.dot(user1, user2.T) / (np.linalg.norm(user1) * np.linalg.norm(user2))
    return cos

def get_users():
    users = [user for user in User.objects.all()]
    return users 

def recommend_user(me):
    my_dict       = get_pkl(me)
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
                user_dict  = get_pkl(user)
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
                print('SORTED =>', recommend_users, '\n')
            # 投稿したことがないユーザの場合の例外処理
            except FileNotFoundError:
                print('"' + str(user) + '"', 'HAS NOT POSTED YET', '\n')
                continue
    # 上位3人のみ取得
    results = {user:sim for user,sim in recommend_users[:3]}
    print('RECOMMEND DICT => ', results, '\n')
    return results
