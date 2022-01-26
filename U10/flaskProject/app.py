from datetime import datetime

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///my_db.db'

db = SQLAlchemy(app)

class ToDo(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Task %r> ' % self.id

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/page/')
def page_fun():
    return render_template("component.html")

if __name__ == '__main__':
    app.run()
