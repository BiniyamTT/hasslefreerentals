#!/usr/local/bin/python3
from telethon import TelegramClient, errors, events, sync
from telethon.tl.types import InputPhoneContact
from telethon import functions, types

import argparse
from getpass import getpass

API_ID = 23009055
API_HASH = 'ded02a65300ccffa08668564650225e1'
PHONE_NUMBER = '+251911600710'

client = TelegramClient('anon', API_ID, API_HASH)
client.connect()


def isontg(phone_number):        
    try:
        contact = InputPhoneContact(client_id = 0, phone = phone_number, first_name="", last_name="")
        contacts = client(functions.contacts.ImportContactsRequest([contact]))
        id = contacts.to_dict()['users'][0]['id']
        if id:
            return True
        else:
            return False
    except IndexError as e:
        return False
    except TypeError as e:
        return False
    except:
        raise

   
numbers = ['+251911600710', '+251911507846', '+251993822334']
for number in numbers:
    result = isontg(number)
    print(result)
        