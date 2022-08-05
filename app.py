from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import flag_modified
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    song = db.Column(db.JSON, nullable=False)

    def __init__(self, title, description, song):
        self.title = title
        self.description = description
        self.song = song


class SongSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "description", "song")


song_schema = SongSchema()
songs_schema = SongSchema(many=True)


@app.route("/song/add", methods=["POST"])
def add_song():
    title = request.json.get("title")
    description = request.json.get("description")
    song = request.json.get("song")

    record = Song(title, description, song)
    db.session.add(record)
    db.session.commit()

    return jsonify(song_schema.dump(record))


@app.route("/song/get", methods=["GET"])
def get_all_songs():
    all_songs = Song.query.all()
    return jsonify(songs_schema.dump(all_songs))


@app.route("/song/<id>", methods=["GET"])
def get_song(id):
    song = Song.query.get(id)
    return jsonify(song_schema.dump(song))


@app.route("/song/<id>", methods=["DELETE"])
def delete_song(id):
    song = Song.query.get(id)
    db.session.delete(song)
    db.session.commit()

    return "Item was successfully deleted"


@app.route("/song/<id>", methods=["PUT"])
def update_song(id):
    song_to_update = Song.query.get(id)

    updated_title = request.json.get("title")
    updated_description = request.json.get("description")
    updated_song = request.json.get("song")

    # db.session.commit()
    # return jsonify(song_schema.dump(song))
    # user = User.query().filter(User.name == 'Jon Dove')
    song_to_update.title = updated_title
    song_to_update.description = updated_description
    song_to_update.song = updated_song
    db.session.commit()
    return jsonify(song_schema.dump(song_to_update))


if __name__ == "__main__":
    app.run(debug=True)
