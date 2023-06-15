from telethon import TelegramClient

# Remember to use your own values from my.telegram.org!
api_id = 23009055
api_hash = 'ded02a65300ccffa08668564650225e1'
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # Getting information about yourself
    me = await client.get_me()

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())
    
    print(await client.get_peer_id('me'))
    
with client:
    client.loop.run_until_complete(main())