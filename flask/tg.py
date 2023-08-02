import re
import os
import requests
import json
import logging
from web3 import Web3
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
# Replace with your Telegram bot token
BOT_TOKEN = "5997630207:AAFFNpcXfMOFGeTV5VdZtLJN6JjAZ1cbQaA"

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()  # Create MemoryStorage instance
dp = Dispatcher(bot, storage=storage)  # Pass the storage to the dispatcher
dp.middleware.setup(LoggingMiddleware())

API_URL = 'http://localhost:5000/tokens'
AMA_URL = 'http://localhost:5000/amas'
INFURA_URL = "https://mainnet.infura.io/v3/8d8396c4e15a4c2fa93a6eea97000b15"
web3 = Web3(Web3.HTTPProvider(INFURA_URL))


def is_valid_address(address):
    return bool(re.match(r'^(0x)[0-9a-fA-F]{40}$', address))


def is_valid_website(website):
    url_pattern = r'^https?://(?:www\.)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/?([^\s]*)$'
    return bool(re.match(url_pattern, website))


class TokenListingForm(StatesGroup):
    contact_address = State()
    logo = State()
    tg_link = State()
    website = State()
    twitter_link = State()
    description = State()


class AMAListingForm(StatesGroup):
    name = State()
    banner = State()
    venue_link = State()
    description = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Welcome to the BOND-007.\n"
                        "/Token: For Token Listing\n"
                        "/AMA: For AMA Listing\n"
                        "/MESSAGE TO BROADCAST MESSAGE")


@dp.message_handler(commands=['Token'])
async def token_listing_handler(message: types.Message, state: FSMContext):
    await message.answer("Please enter the token contact address:")
    await TokenListingForm.contact_address.set()



@dp.message_handler(state=TokenListingForm.contact_address)
async def handle_token_contact_address(message: types.Message, state: FSMContext):
    contact_address = message.text.strip()

    if not is_valid_address(contact_address):
        await message.answer("Invalid contract address format. Please enter a valid Ethereum contract address.")
        return

    async with state.proxy() as data:
        data['contact_address'] = contact_address

    await message.answer("Please send the token logo as a document or a photo:")
    await TokenListingForm.next()


@dp.message_handler(content_types=types.ContentTypes.DOCUMENT, state=TokenListingForm.logo)
async def handle_token_logo_document(message: types.Message, state: FSMContext):
    if message.document.mime_type.startswith('image/'):
        async with state.proxy() as data:
            data['logo_file_id'] = message.document.file_id

        # Download the photo and store it in a specified directory
        file_info = await bot.get_file(message.document.file_id)
        file_path = file_info.file_path
        logo_filename = f"{data['contact_address']}_logo.jpg"
        logo_dir = "static"  # Adjust the directory name as per your project structure
        logo_path = os.path.join(os.getcwd(), logo_dir, logo_filename)

        file = await bot.download_file(file_path)
        with open(logo_path, 'wb') as f:
            f.write(file.read())

        await message.answer("Please send the Telegram link:")
        await TokenListingForm.next()
    else:
        await message.answer("Please upload the token logo as an image document.")


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=TokenListingForm.logo)
async def handle_token_logo_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['logo_file_id'] = message.photo[-1].file_id

    # Download the photo and store it in a specified directory
    file_info = await bot.get_file(data['logo_file_id'])
    file_path = file_info.file_path
    logo_filename = f"{data['contact_address']}_logo.jpg"
    logo_dir = "static"  # Adjust the directory name as per your project structure
    logo_path = os.path.join(os.getcwd(), logo_dir, logo_filename)

    file = await bot.download_file(file_path)
    with open(logo_path, 'wb') as f:
        f.write(file.read())

    await message.answer("Please send the Telegram link:")
    await TokenListingForm.next()


@dp.message_handler(state=TokenListingForm.tg_link)
async def handle_telegram_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tg_link'] = message.text

    await message.answer("Please send the website link:")
    await TokenListingForm.website.set()



@dp.message_handler(state=TokenListingForm.website)
async def handle_website_link(message: types.Message, state: FSMContext):
    website = message.text.strip()

    if not is_valid_website(website):
        await message.answer("Invalid website URL format. Please enter a valid website URL.")
        return

    async with state.proxy() as data:
        data['website'] = website

    await message.answer("Please send the Twitter link:")
    await TokenListingForm.twitter_link.set()


@dp.message_handler(state=TokenListingForm.twitter_link)
async def handle_twitter_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['twitter_link'] = message.text

    await message.answer("Please enter the token description:")
    await TokenListingForm.description.set()


@dp.message_handler(state=TokenListingForm.description)
async def handle_token_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        address=data['contact_address']
        name, symbol = details(address)

        form_data = {
            'contact_address': data['contact_address'],
            'logo': "logo",
            'description': data['description'],
            'name': name,
            'symbol': symbol,
            'tglink': data['tg_link'],
            'website': data['website'],
            'twitterlink': data['twitter_link'],
        }

        response = requests.post(API_URL, json=form_data)

        if response.status_code == 200:
            response_message = f"Token listed!🎊🎊🎊🎊\n\n⚙️Contact Address: {data['contact_address']}\n\n🏷Name: {name}\n" \
                               f"🏷Symbol: {symbol}\n🌐Website: {data['website']}\n🏷Telegram: {data['tg_link']}\n" \
                               f"🏷Twitter: {data['twitter_link']}\n🧾Description: {data['description']}\n"
            await message.answer(response_message)
        else:
            await message.answer("Failed to list the token. Please try again.")

    # Reset state
    await state.finish()


@dp.message_handler(commands=['AMA'])
async def ama_listing_handler(message: types.Message, state: FSMContext):
    await message.answer("Please enter the AMA name:")
    await AMAListingForm.name.set()


@dp.message_handler(state=AMAListingForm.name)
async def handle_ama_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await message.answer("Please send the AMA Banner:")
    await AMAListingForm.banner.set()


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=AMAListingForm.banner)
async def handle_ama_banner(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['banner'] = message.photo[-1].file_id

    await message.answer("Please send the venue link:")
    await AMAListingForm.venue_link.set()


@dp.message_handler(state=AMAListingForm.venue_link)
async def handle_ama_venue_link(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['venue_link'] = message.text

    await message.answer("Please send the description:")
    await AMAListingForm.description.set()


@dp.message_handler(state=AMAListingForm.description)
async def handle_ama_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text

        ama_data = {
            'banner': data['banner'],
            'description': data['description'],
            'name': data['name'],
            'venue_link': data['venue_link'],
        }

        response = requests.post(AMA_URL, json=ama_data)

        if response.status_code == 200:
            response_message = f"AMA listed!\nName: {data['name']}\nDescription: {data['description']}\n" \
                               f"Venue Link: {data['venue_link']}\n"
            await message.answer(response_message)
        else:
            await message.answer("Failed to list the AMA. Please try again.")

    # Reset state
    await state.finish()


@dp.message_handler(lambda message: True)
async def default_handler(message: types.Message):
    await message.reply("I'm sorry, I didn't understand that command.")


def details(contact_address):


    try:

        abi = json.loads('[{"constant":true,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]')
        address = web3.toChecksumAddress(contact_address)

        contract = web3.eth.contract(address=address, abi=abi)

        name=contract.functions.name().call()
        symbol=contract.functions.symbol().call()
        return name,symbol
    except Exception as e:
        logging.exception(e)
        return None, None  # Return None if there's an error in getting the name and symbol


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)