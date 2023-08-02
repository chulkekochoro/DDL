from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os  

app = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'token.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Ama(db.Model):
    __tablename__ = 'amas'

    id = db.Column(db.Integer, primary_key=True)
    banner = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    venue_link = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Ama {self.id}>"

with app.app_context():
    # Create the tokens table
    db.create_all()

if __name__ == '__main__':
    app.run()
