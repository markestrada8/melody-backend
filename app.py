from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
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


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, title, author, description, price):
        self.title = title
        self.author = author
        self.description = description
        self.price = price


class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "title", "author", "description", "price")


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route("/book/add", methods=["POST"])
def add_book():
    title = request.json.get("title")
    author = request.json.get("author")
    description = request.json.get("description")
    price = request.json.get("price")

    record = Book(title, author, description, price)
    db.session.add(record)
    db.session.commit()

    return jsonify(book_schema.dump(record))


@app.route("/book/get", methods=["GET"])
def get_all_books():
    all_books = Book.query.all()
    return jsonify(books_schema.dump(all_books))


@app.route("/book/<id>", methods=["DELETE"])
def delete_book(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return "Item was successfully deleted"


@app.route("/book/<id>", methods=["GET"])
def get_book(id):
    book = Book.query.get(id)
    return jsonify(book_schema.dump(book))


@app.route("/book/<id>", methods=["PUT"])
def update_book(id):
    book = Book.query.get(id)

    book.title = request.json['title']
    book.author = request.json['author']
    book.description = request.json['description']
    book.price = request.json['price']

    db.session.commit()
    return jsonify(book_schema.dump(book))


if __name__ == "__main__":
    app.run(debug=True)
