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

conn = psycopg2.connect(dbname=DB_NAME, user=USER, 
                        password=PASS, host=HOST)
cursor = conn.cursor()

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

# @client.on(events.NewMessage)
# async def handler(event):
#     await event.reply('aa')

# Keyboard generation
def create_keyboard():
    keyboard = [
        [Button.inline('Sport', 'cb_sport'), Button.inline('World', 'cb_world')],
        [Button.inline('US', 'cb_us'), Button.inline('Business', 'cb_business')],
        [Button.inline('Health', 'cb_health'), Button.inline('Entertainment', 'cb_entertainment')],
        [Button.inline('Science & Tech', 'cb_sci_tech')],
        [Button.inline('Get news', 'cb_getnews')]
    ]
    return keyboard

# Handle '/start' 
# Welcome message
@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'INSERT INTO bot_user(chat_id, sport, world,\
                            us, business, health, entertainment, sci_tech)\
                            VALUES ({event.chat_id}, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE)')

    await bot.send_message(event.chat_id, "Hello! I'm CoolstoryBot.\
          What kind of news would you like to receive?", buttons=create_keyboard())

@bot.on(events.NewMessage(pattern='/categories'))
async def send_categories(event):
    await bot.send_message(event.chat_id, 'Here are the categories:', buttons=create_keyboard())


# Handles buttons' clicks
@bot.on(events.CallbackQuery)
async def handler(event):
    # User initialization
    # new_user = User(event.chat_id)
    if event.data == b'cb_sport':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[0].buttons[0].text[-1] == '✅':
            markup.rows[0].buttons[0].text = 'Sport'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[0].buttons[0].text = 'Sport ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])
        
        await msg.edit(buttons=markup)

        await event.answer(status)    

    elif event.data == b'cb_world':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[0].buttons[1].text[-1] == '✅':
            markup.rows[0].buttons[1].text = 'World'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[0].buttons[1].text = 'World ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                                
        await event.answer(status)  

    elif event.data == b'cb_us':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[1].buttons[0].text[-1] == '✅':
            markup.rows[1].buttons[0].text = 'US'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[1].buttons[0].text = 'US ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                                
        await event.answer(status)

    elif event.data == b'cb_business':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[1].buttons[1].text[-1] == '✅':
            markup.rows[1].buttons[1].text = 'Business'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[1].buttons[1].text = 'Business ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                                
        await event.answer(status)  

    elif event.data == b'cb_health':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[2].buttons[0].text[-1] == '✅':
            markup.rows[2].buttons[0].text = 'Health'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[2].buttons[0].text = 'Health ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                              
        await event.answer(status)  
    
    elif event.data == b'cb_entertainment':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[2].buttons[1].text[-1] == '✅':
            markup.rows[2].buttons[1].text = 'Entertainment'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[2].buttons[1].text = 'Entertainment ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                                
        await event.answer(status)  
        
    elif event.data == b'cb_sci_tech':
        msg    = await event.get_message()
        markup = msg.reply_markup
        status = ''
        if markup.rows[3].buttons[0].text[-1] == '✅':
            markup.rows[3].buttons[0].text = 'Science & Tech'
            status = CATEGORY_RM_MSG
            # new_user.selected_categories.remove(event.data[3:])
        else:
            markup.rows[3].buttons[0].text = 'Science & Tech ✅'
            status = CATEGORY_ADD_MSG
            # new_user.selected_categories.append(event.data[3:])

        await msg.edit(buttons=markup) 
                                                                                
        await event.answer(status)  

    else:
        await event.answer('Got the news!')

    # #Add new user to the list
    # if call.message.chat.id not in id_list:
    #     new_user.subscribed = True #start sending news
    #     id_list.append(new_user.chat_id)
    #     user_list.append(new_user)


client.run_until_disconnected()
bot.run_until_disconnected()        