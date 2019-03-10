# Mimic-Instagram

## Create an application that is not ashamed to show to people as a portfolio.

### Description
- Create SNS with Django
  - Instagram tribute
- Labeling posted images using vgg16
- Compute similarity of user's tastes based on posted images, implement user's recommendation
- Acquire similar users of similar users and draw network diagrams

## Preview
### Index pages
![Imgur](https://i.imgur.com/UN5p3N9.gif)  
`Imagenet inference` is Inference result of vgg16  
`Probability` is Probability of the above inference  

### Post Image
![Imgur](https://i.imgur.com/YhWezYq.gif)

### Recommend Users
The most important feature is user base filtering from the user's posted image and recommends similar users  
![Imgur](https://i.imgur.com/b7sowfW.png)

### Setup
`$ mkdir <YOUR DIR> && cd <YOUR DIR>`  
`$ python -m venv venv`  
`$ source venv/bin/activate`  
`$ git clone git@github.com:10380r/Mimic-Instagram.git`  
`$ cd Mimic-Instagram`  
`$ pip install -r requirements.txt`  
Rewrite  
https://github.com/10380r/Mimic-
Instagram/blob/ebe7eb0c48ccba39c4ab40b6f56e797b9b8a5e24/app/recommend_user.py#L5  
to Path to Mimic-Instagram  
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
