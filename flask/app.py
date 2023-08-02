from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

import os  

APP = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'token.db')
db_uri = 'sqlite:///{}'.format(db_path)
APP.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(APP)

class Tokens(db.Model):
    __tablename__ = 'tokens'

    id = db.Column(db.Integer, primary_key=True)
    contact_address = db.Column(db.String(255), nullable=False)
    logo = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    symbol = db.Column(db.String(255), nullable=False)
    tglink = db.Column(db.String(255), nullable=False)
    website = db.Column(db.String(255), nullable=False)
    twitterlink = db.Column(db.String(255), nullable=False)

    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Tokens {self.id}>"

    def __init__(self, contact_address, logo, description, name, symbol, tglink, website, twitterlink):
        self.contact_address = contact_address
        self.logo = logo
        self.description = description
        self.name = name
        self.symbol = symbol
        self.tglink = tglink
        self.website = website
        self.twitterlink = twitterlink


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

    def __init__(self, banner, description, name, venue_link):
        self.banner = banner
        self.description = description
        self.name = name
        self.venue_link = venue_link


# Endpoint for inserting token data
@APP.route('/tokens', methods=['POST'])
def insert_token():
    try:
        # Get the token data from the request body
        token_data = request.json

        # Extract the required fields
        contact_address = token_data.get('contact_address')
        logo = token_data.get('logo')
        description = token_data.get('description')
        name = token_data.get('name')
        symbol = token_data.get('symbol')
        tglink = token_data.get('tglink')
        website = token_data.get('website')
        twitterlink = token_data.get('twitterlink')

        # Create a new Token object
        token = Tokens(contact_address=contact_address, logo=logo, description=description, name=name, symbol=symbol,tglink=tglink,website=website,twitterlink=twitterlink)

        # Perform the database insertion
        db.session.add(token)
        db.session.commit()

        # Return a success response
        response = {
            'message': 'Token listed successfully!'
        }
        return jsonify(response), 200

    except SQLAlchemyError as e:
        # Rollback the transaction in case of an exception
        db.session.rollback()

        # Return an error response with the specific database-related error message
        response = {
            'message': f"Database error: {str(e)}"
        }
        return jsonify(response), 400

    except Exception as e:
        # Return a generic error response for any other exception
        response = {
            'message': f"An error occurred: {str(e)}"
        }
        return jsonify(response), 400


@APP.route('/amas', methods=['POST'])
def insert_ama():
    try:
        # Get the token data from the request body
        ama_data = request.json

        # Extract the required fields
        banner = ama_data.get('banner')
        description = ama_data.get('description')
        name = ama_data.get('name')
        venue_link = ama_data.get('venue_link')


        # Create a new Token object
        ama = Ama( banner=banner, description=description, name=name, venue_link=venue_link)

        # Perform the database insertion
        db.session.add(ama)
        db.session.commit()

        # Return a success response
        response = {
            'message': 'ama listed successfully!'
        }
        return jsonify(response), 200

    except:
        # Return an error response if something goes wrong
        response = {
            'message': 'Failed to list the ama. Please try again.'
        }
        return jsonify(response), 400

@APP.route('/')
def page():
    tokens =Tokens.query.limit(12).all()
    amas =Ama.query.limit(6).all()
    return render_template('index.html', tokens=tokens, amas=amas)




if __name__ == '__main__':
    APP.debug=True
    APP.run()
