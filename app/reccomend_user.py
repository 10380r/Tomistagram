import numpy as np
import pickle
import pandas as pd
import django
import os,sys

def get_user(file):
    with open(file, 'rb') as f:
        print(pickle.load(f))

def sim_cos(user1, user2):
    cos = np.dot(user1, user2.T) / (np.linalg.norm(user1) * np.linalg.norm(user2))
    return cos

def main():
    # ローカルでmodelを扱えるようにする
    sys.path.append('/Users/tommy/src/develop/mimicstagram/mimicstagram/')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mimicstagram.settings')  # 自分のsettings.py
    django.setup()
    from app.models import User
    for user in User.objects.all():
        print(user)

if __name__ =='__main__':
    main()
