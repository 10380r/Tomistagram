import numpy as np
import pickle
import pandas as pd

def get_user(file):
    with open(file, 'rb') as f:
        a = pickle.load(f)
        print(a)
#    a = pd.read_pickle(file)
#    print(a)

def sim_cos(user1, user2):
    cos = np.dot(user1, user2.T) / (np.linalg.norm(user1) * np.linalg.norm(user2))
    return cos

if __name__ =='__main__':
    get_user('./pickles/Ryunosuke_Tomiyama.pkl')
