import telebot
import configparser

from apitok import API_TOKEN
from classifier import get_en_news_category
from telethon.tl.functions.channels import JoinChannelRequest
from user import User

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from telethon import events, TelegramClient

config = configparser.ConfigParser()
config.read("config.ini")

user_list = []
id_list = []

CATEGORY_ADD_MSG = 'Category added!'
CATEGORY_RM_MSG  = 'Category removed!'

# Присваиваем значения внутренним переменным
api_id   = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
username = config['Telegram']['username']

client = TelegramClient(username, api_id, api_hash).start()

bot = TelegramClient('CoolStoryBot', api_id, api_hash).start(bot_token=API_TOKEN)


@client.on(events.NewMessage())
async def handler(event):
    # Respond whenever someone says "Hello" and something else
    await event.reply('aa')


# Handle '/start' 
# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I'm CoolstoryBot. What kind of news would you like to receive?", reply_markup=gen_markup())

       
# Handle '/help'
# Commands list
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, '\n/start\n/change\n/help') 


# Keyboard generation
def gen_markup():
    markup = InlineKeyboardMarkup()
    #markup.row_width = 2
    markup.row(InlineKeyboardButton('Sport', callback_data='cb_sport'),
                InlineKeyboardButton('World', callback_data='cb_world'))
    markup.row(InlineKeyboardButton('US', callback_data='cb_us'),
                InlineKeyboardButton('Business', callback_data='cb_business'))
    markup.row(InlineKeyboardButton('Health', callback_data='cb_health'),
                InlineKeyboardButton('Entertainment', callback_data='cb_entertainment'))
    markup.add(InlineKeyboardButton('Science & Tech', callback_data='cb_sci_tech'))
    markup.add(InlineKeyboardButton('Get news', callback_data='cb_getnews'))
    return markup


# Creates keyboard on click
@bot.message_handler(commands=['change'])
def start_message2(message):
    bot.send_message(message.chat.id, 'Categories:', reply_markup=gen_markup())


# Handles buttons' clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    #User initialization
    new_user = User(call.message.chat.id)

    if call.data == 'cb_sport':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[0][0].text[-1] == '✅':
            markup.keyboard[0][0].text = 'Sport'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[0][0].text = 'Sport ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])
            
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)    

    elif call.data == 'cb_world':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[0][1].text[-1] == '✅':
            markup.keyboard[0][1].text = 'World'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[0][1].text = 'World ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_us':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[1][0].text[-1] == '✅':
            markup.keyboard[1][0].text = 'US'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[1][0].text = 'US ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)

    elif call.data == 'cb_business':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[1][1].text[-1] == '✅':
            markup.keyboard[1][1].text = 'Business'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[1][1].text = 'Business ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_health':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[2][0].text[-1] == '✅':
            markup.keyboard[2][0].text = 'Health'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[2][0].text = 'Health ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
    
    elif call.data == 'cb_entertainment':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[2][1].text[-1] == '✅':
            markup.keyboard[2][1].text = 'Entertainment'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[2][1].text = 'Entertainment ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
        
    elif call.data == 'cb_sci_tech':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[3][0].text[-1] == '✅':
            markup.keyboard[3][0].text = 'Science & Tech'
            status = CATEGORY_RM_MSG
            new_user.selected_categories.remove(call.data[3:])
        else:
            markup.keyboard[3][0].text = 'Science & Tech ✅'
            status = CATEGORY_ADD_MSG
            new_user.selected_categories.append(call.data[3:])

        bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                        message_id=call.message.id, 
                                        reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    else:
        bot.answer_callback_query(call.id, 'Got the news!')
        
        #Add new user to the list
        if call.message.chat.id not in id_list:
            new_user.subscribed = True #start sending news
            id_list.append(new_user.chat_id)
            user_list.append(new_user)

bot.polling(none_stop=True)
client.run_until_disconnected()
bot.run_until_disconnected()        