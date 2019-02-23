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
    most_sim, second_sim, third_sim  = 0, 0, 0
    most_sim_user, second_sim_user, third_sim_user = '', '', ''
    for user in users:
        if user == me:
            continue
        else:
            try:
                user_dict  = get_pkl(user)
                user_array = np.fromiter(user_dict.values(), dtype=float)
                similarity = sim_cos(my_array, user_array)
                if most_sim < similarity:
                    most_sim        = similarity
                    most_sim_user   = user
                    print('1: ', most_sim_user)
                elif second_sim < similarity:
                    second_sim      = similarity
                    second_sim_user = user
                    print('2: ', second_sim_user)
                elif third_sim < similarity:
                    third_sim       = similarity
                    third_sim_user  = user
                    print('3: ', third_sim_user)
            except FileNotFoundError:
                continue

    results = {'most_sim_user':most_sim, 'second_sim_user':second_sim, 'third_sim_user':third_sim}
    return results
