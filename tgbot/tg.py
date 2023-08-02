import sqlite3
import telebot
import requests
import json
from web3 import Web3


# Create a bot instance
bot = telebot.TeleBot("5997630207:AAFFNpcXfMOFGeTV5VdZtLJN6JjAZ1cbQaA")
API_URL = 'http://localhost:5000/tokens'  # Replace with your API endpoint URL
infura_url = "https://mainnet.infura.io/v3/8d8396c4e15a4c2fa93a6eea97000b15"
web3 = Web3(Web3.HTTPProvider(infura_url))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the BOND-007.\n/Token: For Token Listing")

@bot.message_handler(commands=['Token'])
def token_listing_handler(message):
    chat_id = message.chat.id
    
    # Send a message to the user asking for the token contact address
    bot.send_message(chat_id, "Please enter the token contact address:")
    
    # Register a new message handler to handle the token contact address
    bot.register_next_step_handler(message, handle_token_contact_address)

def handle_token_contact_address(message):
    contact_address = message.text
    
    # Send a message to the user asking for the token logo
    bot.send_message(message.chat.id, "Please send the token logo:")
    
    # Register a new message handler to handle the token logo
    bot.register_next_step_handler(message, handle_token_logo, contact_address)

def handle_token_logo(message, contact_address):
    # Assuming the logo is sent as a photo, you can access it using `message.photo`
    logo = message.photo[-1].file_id
    
    # Send a message to the user asking for the token description
    bot.send_message(message.chat.id, "Please send the telegram link")
    
    # Register a new message handler to handle the token description
    bot.register_next_step_handler(message, handle_telegram_link, contact_address, logo)

def handle_telegram_link(message, contact_address, logo):

    tglink = message.text
    
    # Send a message to the user asking for the token logo
    bot.send_message(message.chat.id, "Please send the website link:")
    
    # Register a new message handler to handle the token description
    bot.register_next_step_handler(message, handle_website_link, contact_address, logo, tglink)

def handle_website_link(message, contact_address, logo, tglink):

    website = message.text
    
    # Send a message to the user asking for the token logo
    bot.send_message(message.chat.id, "Please send the twitter link:")
    
    # Register a new message handler to handle the token description
    bot.register_next_step_handler(message, handle_twitter_link, contact_address, logo, tglink, website)

def handle_twitter_link(message, contact_address, logo, tglink, website):

    twitterlink = message.text
    
    # Send a message to the user asking for the token logo
    bot.send_message(message.chat.id, "Please enter the token description:")
    
    # Register a new message handler to handle the token description
    bot.register_next_step_handler(message, handle_token_description, contact_address, logo, tglink, website, twitterlink)

def handle_token_description(message, contact_address, logo, tglink, website, twitterlink):
    description = message.text
    name, symbol = details()
    # Send a request to the API to insert the token data into the database
    data = {
        'contact_address': contact_address,
        'logo': logo,
        'description': description,
        'name': name,
        'symbol': symbol,
        'tglink': tglink,
        'website': website,
        'twitterlink': twitterlink,

    }
    response = requests.post(API_URL, json=data)
    
    
    if response.status_code == 200:
    	response_message = f"Token listed!\n\n⚙️Contact Address: {contact_address}\n\nName: {name}\nSymbol: {symbol}\nTelegram: {tglink}\n🌐website: {website}\nTwitter: {twitterlink}\nDescription: {description}\n"
    	bot.send_message(message.chat.id, response_message)
    else:
        bot.send_message(message.chat.id, "Failed to list the token. Please try again.")

@bot.message_handler(func=lambda message: True)
def default_handler(message):
    # Handle any other commands or messages
    bot.reply_to(message, "I'm sorry, I didn't understand that command.")

def details():

	# OMG Address
	abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
	# OMG ABI
	address = '0xA09bf9bE74aD44bd5cF56fb97191492Ce92194aC'

	contract = web3.eth.contract(address=address, abi=abi)

	name=contract.functions.name().call()
	symbol=contract.functions.symbol().call()

	return name,symbol


# Start the bot
bot.polling()