from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os  

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'token.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    elon = db.Column(db.String(255), nullable=False)
    vitalk = db.Column(db.String(255), nullable=False)
    cz = db.Column(db.String(255), nullable=False)


    def __repr__(self):
        return f"<Message {self.id}>"

with app.app_context():
    # Create the tokens table
    db.create_all()

if __name__ == '__main__':
    app.run()
