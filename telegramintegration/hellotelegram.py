from telethon import TelegramClient

# Use your own values from my.telegram.org
api_id = 23009055
api_hash = 'ded02a65300ccffa08668564650225e1'
phone = '+251911600710'

# The first parameter is the .session file name (absolute paths allowed)
with TelegramClient('hasslefreerentals', api_id, api_hash) as client:
    client.loop.run_until_complete(client.send_message(phone, 'Hello, myself!'))