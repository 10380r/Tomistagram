# Mimic-Instagram

## Create an application that is not ashamed to show to people as a portfolio.

### Description
This application is a **Matching SNS** created based on Instagram's philosophy.  
Label the image posted by the user with vgg16.  
Next, calculate the similarity between users based on the label, and recommend users in order of similarity.  

> VGG 16 is a 16-layer CNN model learned with a large-scale image dataset called "ImageNet." It was announced in 2014. It is a famous It is one of the learned models  

- このアプリケーションは、インスタグラムの思想をベースに作られた**マッチング系SN**Sです。  
- ユーザーが投稿した画像に対して、vgg16でラベル付けをします。  
- 次に、ラベルを元にユーザ同士の類似度を計算して、類似度順にユーザをレコメンドします。  

 > VGG16というのは，「ImageNet」と呼ばれる大規模画像データセットで学習された，16層からなるCNNモデルのことです．2014年に発表されました．  
 > 様々な研究で利用されている，有名な学習済みモデルの1つです


## Preview
  ### Index pages
  ![Imgur](https://i.imgur.com/yrTnLXI.gif)  
  `Imagenet inference` is Inference result of vgg16  
  `Probability` is Probability of the above inference  
  
  
  ### Post Image
  ![Imgur](https://i.imgur.com/DVe92po.gif)  
  
  ### Recommend Users
  The most important feature is user base filtering from the user's posted image and recommends similar users  
  ![Imgur](https://i.imgur.com/b7sowfW.png)  
  
  ### User page
  ![Imgur](https://i.imgur.com/a6e9nGa.png)

### Setup
`$ mkdir <YOUR DIR> && cd <YOUR DIR>`  
`$ python -m venv venv`  
`$ source venv/bin/activate`  
`$ git clone git@github.com:10380r/Mimic-Instagram.git`  
`$ cd Mimic-Instagram`  
`$ pip install -r requirements.txt`  
`$ ./manage.py migrate`  
`$ ./manage.py createsuperuser`  
`$ ./manage.py runserver`  

login at [admin page](http://localhost:8000/admin)
  - create users
    > _Notes: When entering User information, change the permission to Staff status. Also select Choose all for User permission._

Then, you can try sns. at http://localhost:8000/app

### Requirements
See [reqirements.txt](https://github.com/10380r/Mimic-Instagram/blob/master/requirements.txt) for details  
`python 3.7.2`  
`django 2.1.5`  
`Mac OS Mojave 10.14.3` (I am trying to execute it only on this OS)  

### References
[vgg16](https://keras.io/ja/applications/#vgg1://keras.io/ja/applications/#vgg16)  
[vue.js network](http://visjs.org/docs/network/) You can change the drawing style of the network by changing vue.
