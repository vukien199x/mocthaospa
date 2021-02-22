from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_wtf import CSRFProtect

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["WTF_CSRF_SECRET_KEY"] = 'KinS2Din'
app.config["SECRET_KEY"] = 'DinS2Kin'
CSRFProtect(app)
db = SQLAlchemy(app)
session = db.session


class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff = db.Column(db.String)
    customer = db.Column(db.String)
    phone = db.Column(db.String)
    comment = db.Column(db.String)
    feed_back = db.Column(db.String)
    created_at = db.Column(db.DATETIME, default=datetime.utcnow())


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/comment', methods=['POST'])
def comment():
    cmt = Comment(**request.get_json())
    session.add(cmt)
    session.commit()
    return 'Cảm ơn sự đánh giá và góp ý của quý khách hàng!'


@app.route('/all_comment')
def comment_home():
    comments = Comment.query.all()
    for cm in comments:
        cm.feed_back = range(0, int(cm.feed_back))
    return render_template('comment.html', comments=comments)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=6868)
