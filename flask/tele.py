  # Replace with destination channel username
import re
from telethon import TelegramClient, events, types

api_id="26783614"
api_hash="3be11c61f043106312cf22a43edb9662"

client = TelegramClient('telethon', api_id, api_hash)

async def resolve_destination():
    # Change the entity ID to your private group ID where you want to forward the messages
    entity = await client.get_entity('thirteenpoint5')
    return entity

async def is_relevant_amount(message_text):
    # Regular expression pattern to match amounts close to 13.4 or 13.5
    pattern = r'13\.(4[0-9]|5[0-2])\s*SOL' 
    empty_pattern = r''
    return re.search(pattern, message_text, re.IGNORECASE) is not None

@client.on(events.NewMessage(chats='newsolanatokens', incoming=True))
async def forward_images(event):
    try:
        destination_entity = await resolve_destination()
        if destination_entity and event.media:
            message_text = event.text
            if await is_relevant_amount(message_text):
                await client.forward_messages(destination_entity.id, event.message)
                print(f"Image forwarded: {event.text}")
    except Exception as e:
        print(f"Error while forwarding image: {e}")

async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())