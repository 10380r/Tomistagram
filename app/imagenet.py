# encoding:utf-8
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
import numpy as np
import sys

def imagenet(file):
    model = VGG16(weights='imagenet')
    # 入力するデータを読み込み整形
    img = image.load_img(file, target_size=(224, 224))
    # 画像を配列に変換
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    # モデルにかけて推論
    preds = model.predict(preprocess_input(x))
    #推論結果
    results = decode_predictions(preds)
    return results
