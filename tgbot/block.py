from moralis import evm_api
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from web3 import Web3
from threading import Thread
import os
import json
import time

APP = Flask(__name__)
db_path = os.path.join(os.path.dirname(__file__), 'token.db')
db_uri = 'sqlite:///{}'.format(db_path)
APP.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(APP)

class Token(db.Model):
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
    rank = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Token {self.id}>"

    def __init__(self, contact_address, logo, description, name, symbol, tglink, website, twitterlink, rank):
        self.contact_address = contact_address
        self.logo = logo
        self.description = description
        self.name = name
        self.symbol = symbol
        self.tglink = tglink
        self.website = website
        self.twitterlink = twitterlink
        self.rank = rank
contract_addresses = Token.query.with_entities(Token.contact_address).all()

print(contract_addresses)
if __name__ == '__main__':
    APP.debug=True
    APP.run()
