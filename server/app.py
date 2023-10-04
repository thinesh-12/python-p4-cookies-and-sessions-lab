#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route("/articles")
def index_articles():
    arts = [art.to_dict() for art in Article.query.all()]
    response = make_response(arts, 200)
    return response


@app.route("/articles/<int:id>")
def show_article(id):
    art = Article.query.filter(Article.id == id).first().to_dict()

    session["page_views"] = (
        session["page_views"] + 1 if session.get("page_views") else 1
    )

    if session.get("page_views") <= 3:
        response = make_response(art, 200)
        return response

    elif session.get("page_views") > 3:
        message = {"message": "Maximum pageview limit reached"}
        response = make_response(message, 401)
        return response

if __name__ == '__main__':
    app.run(port=5556)
