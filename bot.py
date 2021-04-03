import configparser
import psycopg2
from dbconfig import *
from apitok import API_TOKEN
from classifier import get_en_news_category
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.custom import Button
from user import User
from telethon import events, TelegramClient
from contextlib import closing

table = 'bot'
config = configparser.ConfigParser()
config.read('config.ini')

CATEGORY_ADD_MSG = 'Category added!'
CATEGORY_RM_MSG  = 'Category removed!'

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash).start()

bot = TelegramClient('CoolStoryBot', api_id, api_hash).start(bot_token=API_TOKEN)

@client.on(events.NewMessage(chats=[-1001317428262]))
async def news_handler(event):
    await client.forward_messages(1436454776, event.message)

# Language keyboard generation
def create_lang_keyboard(chat_id):
    user_entry=[]
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT * FROM bot_user WHERE chat_id = {chat_id}')
            user_entry = cursor.fetchall()
    en = ' ✅' if user_entry[0][-1]==True else ''
    ru = ' ✅' if user_entry[0][-1]==False else ''
    keyboard = [Button.inline(f'Русский{ru}', 'cb_ru'), Button.inline(f'English{en}', 'cb_en')]
    return keyboard

# Categories keyboard generation
def create_keyboard(chat_id):
    user_entry = []
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT * FROM bot_user WHERE chat_id = {chat_id}')
            user_entry = cursor.fetchall()
    ctgrs = [' ✅' if user_entry[0][i]==True else '' for i in range(0, 7)]
    en = ' ✅' if user_entry[0][-1]==True else ''
    ru = ' ✅' if user_entry[0][-1]==False else ''
    keyboard = [
        [Button.inline(f'Sport{ctgrs[0]}', 'cb_sport'), Button.inline(f'World{ctgrs[1]}', 'cb_world')],
        [Button.inline(f'US{ctgrs[2]}', 'cb_us'), Button.inline(f'Business{ctgrs[3]}', 'cb_business')],
        [Button.inline(f'Health{ctgrs[4]}', 'cb_health'), Button.inline(f'Entertainment{ctgrs[5]}', 'cb_entertainment')],
        [Button.inline(f'Science & Tech{ctgrs[6]}', 'cb_sci_tech')],
        [Button.inline(f'Русский{ru}', 'cb_ru'), Button.inline(f'English{en}', 'cb_en')]
    ]
    return keyboard

# Handle '/start' 
# Welcome message
@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT * FROM bot_user WHERE chat_id = {event.chat_id}')
            user_entry = cursor.fetchall()
            if len(user_entry)==0:
                cursor.execute(f'INSERT INTO bot_user(chat_id, sport, world,us, business, health, entertainment, sci_tech)\
                VALUES ({event.chat_id}, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE)')
    await bot.send_message(event.chat_id, "Hello! I'm CoolstoryBot. What kind of news would you like to receive?", buttons=create_keyboard(event.chat_id))

@bot.on(events.NewMessage(pattern='/categories'))
async def send_categories(event):
    await bot.send_message(event.chat_id, 'Here are the categories:', buttons=create_keyboard(event.chat_id))

@bot.on(events.NewMessage(chats=[1724712563]))
async def client_handler(event):
    msg = event.message.message.split('\n')[0]
    ctg = get_en_news_category(msg)

    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT chat_id FROM bot_user WHERE {ctg} = TRUE')
            sub_users = cursor.fetchall()

            for user in sub_users:
                await bot.forward_messages(user[0], event.message)

# Handles buttons' clicks
@bot.on(events.CallbackQuery)
async def keyboard_handler(event):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            
            btns = {b'cb_sport'        : 'Sport',
                    b'cb_world'        : 'World',
                    b'cb_us'           : 'US',
                    b'cb_business'     : 'Business',
                    b'cb_health'       : 'Health',
                    b'cb_entertainment': 'Entertainment',
                    b'cb_sci_tech'     : 'Science & Tech',
                    b'cb_ru'           : 'Русский',
                    b'cb_eb'           : 'English'}
            
            pos = 0
            for key, name in btns.items():
                if event.data == key:
                    key = key.decode('UTF-8')
                    msg    = await event.get_message()
                    markup = msg.reply_markup
                    status = ''
                    if markup.rows[pos//2].buttons[pos%2].text[-1] == '✅':
                        markup.rows[pos//2].buttons[pos%2].text = name
                        status = CATEGORY_RM_MSG
                        cursor.execute(f'UPDATE bot_user SET {key[3:]} = FALSE WHERE chat_id = {event.chat_id}')
                    else:
                        markup.rows[pos//2].buttons[pos%2].text = f'{name} ✅'
                        status = CATEGORY_ADD_MSG
                        cursor.execute(f'UPDATE bot_user SET {key[3:]} = TRUE WHERE chat_id = {event.chat_id}')
                    
                    await msg.edit(buttons=markup)

                    await event.answer(status)
                    break
                pos += 1

client.run_until_disconnected()
bot.run_until_disconnected()        