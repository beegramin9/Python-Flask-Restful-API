## 모듈 설치

pip install -r requirements.txt

## 실행

python main.py

1. Postman와 같은 API platform이 설치되어 사용할 수 있을 때
   localhost:5000에서 get, post, patch, delete 요청을 선택하여 API의 작동을 확인할 수 있습니다. post 요청일 때는 Body 파라미터의 Content-Type = x-www-form-urlencoded로 파라미터를 보내면 됩니다.

2. API platform을 사용할 수 없을 때

- python test.py
  mock-up 데이터가 준비되어 있습니다. requests 모듈로 http://127.0.0.1:5000/에 get, post, patch, delete 요청을 보내 API의 작동을 확인할 수 있습니다.

## Project Status

![Generic badge](https://img.shields.io/badge/build-passing-green.svg)

## Overview

![Flask](https://user-images.githubusercontent.com/58083434/131241846-68a75bb6-3ab1-4378-a937-6d3fac058cf7.gif)

## Technology Stack

<img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>&nbsp;
<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=Flask&logoColor=white"/></a>&nbsp;
<img src="https://img.shields.io/badge/SQLAlchemy-CC2927?style=flat-square&logo=Databricks&logoColor=white"/></a>&nbsp;

## Outline

&nbsp; This is a simple Restful API built with Flask and SQLAlchemy. SQLAlchemy supports ORM designed to fully support CRUD interactions easily.

<br/>
&nbsp; Flask와 SQLAlchemy로 만들어진 간단한 Restful API입니다. SQLAlchemy는 CRUD를 위한 ORM(객체 관계 매핑)을 지원합니다.

## Main Feature Code

- VideoModel 생성 <br/>
  > (/main.py) <br/>
  > 데이터베이스의 모델을 생성합니다. <br/>

```python
db = SQLAlchemy(app)
# config the location of the db, :///database.db이름 (relative path)
app.config['SQLAlCHEMY_DATABASE_URI'] = "sqlite:///database.db"

# Set up a model
class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    views = db.Column(db.Integer, nullable=False)
    likes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Video name:{self.name}, views={self.views}, likes={self.likes}'

# Model initializing
db.create_all()
# 서버가 처음 만들어질 때 한번만 해야 한다. Otherwise it overrides the exisiting data
```

- Request Parsing <br/>
  > (/main.py) <br/>
  > flask.request object 파라미터의 type, error message, 필수 여부를 설정할 수 있습니다. <br/>

```python
video_post_args = reqparse.RequestParser()
# 개발자 임의대로 설정 가능합니다
# 여기서는 모델_요청_args의 형식을 따랐습니다.
video_post_args.add_argument('name',
                             type=str,
                             help="Error: Name of the video is required.",
                             required=True)
video_post_args.add_argument('views',
                             type=int,
                             help="Error: Views of the video is required.",
                             required=True)
video_post_args.add_argument('likes',
                             type=int,
                             help="Error: Likes of the video is required.",
                             required=True)

video_patch_args = reqparse.RequestParser()
video_patch_args.add_argument('name', type=str)
video_patch_args.add_argument('views', type=int)
video_patch_args.add_argument('likes', type=int)
```
