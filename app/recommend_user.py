import numpy as np
import pickle,django,os,sys

def get_pkl(user):
    with open('pickles/%s.pkl' %(user), 'rb') as f:
        return pickle.load(f)

def sim_cos(user1, user2):
    cos = np.dot(user1, user2.T) / (np.linalg.norm(user1) * np.linalg.norm(user2))
    return cos

def get_users():
     # ローカルでmodelを扱えるようにする
    sys.path.append('/Users/tommy/src/develop/mimicstagram/mimicstagram/')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mimicstagram.settings')  # 自分のsettings.py
    django.setup()
    from app.models import User
    users = [user for user in User.objects.all()]
    return users 

def recommend_user(me):
    my_dict       = get_pkl(me)
    my_array      = np.fromiter(my_dict.values(), dtype=float)
    users         = get_users()
    most_sim      = 0
    most_sim_user = ''
    for user in users:
        if user == me:
            continue
        else:
            try:
                user_dict  = get_pkl(user)
                user_array = np.fromiter(user_dict.values(), dtype=float)
                similarity = sim_cos(my_array, user_array)
                if most_sim < similarity:
                    most_sim      = similarity
                    most_sim_user = user
                    print(most_sim_user)
            except FileNotFoundError:
                continue

    return most_sim, most_sim_user
