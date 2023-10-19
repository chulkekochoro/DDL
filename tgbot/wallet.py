import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

# Set up logging
logging.basicConfig(level=logging.INFO)

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6236270240:AAFEXUwKYrcX3djmOY9bhdrMHG3UmE41Hls'

# Initialize the bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Define the /start command handler
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user = message.from_user
    await message.reply(f"Hello, {user.first_name}! I'm your simple bot.")

# Define the /hello command handler
@dp.message_handler(commands=['hello'])
async def hello(message: types.Message):
    await message.reply("Hello there! How can I assist you today?")

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
