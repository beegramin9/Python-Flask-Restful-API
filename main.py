from flask import Flask
import requests
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)


# Mockup Api
class HelloWorld(Resource):
    def get(self, name):
        return {"name": name}

    def post(self):
        return {"data": "Posted"}


# config the location of the db, :///database.db이름 (relative path)
app.config['SQLAlCHEMY_DATABASE_URI'] = "sqlite:///database.db"

db = SQLAlchemy(app)


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

video_post_args = reqparse.RequestParser()
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
# update된게 없으면 자동으로 그 값을 None으로 채운다

# def abort_if_video_id_not_exist(video_id):
#     if video_id not in videos:
#         abort(404, message='Video id not exist.')

# def abort_if_video_already_exist(video_id):
#     if video_id in videos:
#         abort(409, message=f'Video {video_id} already exists.')

# how to serializate, Dictionary => Json
resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer
}


class Video(Resource):
    # marshal with: to arrange or assemble things in order
    # Model에서 return되는 object가 있다면 반드시 필요
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video {video_id} not exist")
        return result

    @marshal_with(resource_fields)
    def post(self, video_id):
        args = video_post_args.parse_args()
        existing_video = VideoModel.query.filter_by(
            id=video_id).first()  # not json, unfortunately dictionary
        if existing_video:
            abort(409, message=f"Video {video_id} already exist")
        video = VideoModel(id=video_id,
                           name=args['name'],
                           views=args['views'],
                           likes=args['likes'])

        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_fields)
    def patch(self, video_id):
        args = video_patch_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, message="Video {video_id} not exist")

        if args['name']:
            VideoModel.name = args['name']
        if args['views']:
            VideoModel.views = args['views']
        if args['likes']:
            VideoModel.likes = args['likes']

        # 이미 session에 있다면 db.session.add(video) 필요없다
        db.session.commit()
        return result

    def delete(self, video_id):
        existing_video = VideoModel.query.filter_by(id=video_id).first()
        if not existing_video:
            abort(404, message="Video {video_id} not exist")

        db.session.delete(existing_video)
        db.session.commit()
        return {'message': 'Successfully deleted'}, 204


# Api 등록
api.add_resource(HelloWorld, '/helloworld/<string:name>')
api.add_resource(Video, '/video/<int:video_id>')

if __name__ == "__main__":
    app.run(debug=True)
