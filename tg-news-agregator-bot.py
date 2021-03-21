import telebot
from Classifier import getEnNewsCategory
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1436454776:AAGlRrnESJA4ih1yGia4fGy9EcsIwsIqB3w'

bot = telebot.TeleBot(API_TOKEN)

category_add_msg = 'Category added!'
category_rm_msg  = 'Category removed!'

# Handle '/start' 
# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Hello! I'm CoolstoryBot.", reply_markup=gen_markup())

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
    # call.chat_instance
    if call.data == 'cb_sport':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[0][0].text[-1] == '✅':
            markup.keyboard[0][0].text = 'Sport'
            status = category_rm_msg
        else:
            markup.keyboard[0][0].text = 'Sport ✅'
            status = category_add_msg
            
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)    

    elif call.data == 'cb_world':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[0][1].text[-1] == '✅':
            markup.keyboard[0][1].text = 'World'
            status = category_rm_msg
        else:
            markup.keyboard[0][1].text = 'World ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_us':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[1][0].text[-1] == '✅':
            markup.keyboard[1][0].text = 'US'
            status = category_rm_msg
        else:
            markup.keyboard[1][0].text = 'US ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)

    elif call.data == 'cb_business':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[1][1].text[-1] == '✅':
            markup.keyboard[1][1].text = 'Business'
            status = category_rm_msg
        else:
            markup.keyboard[1][1].text = 'Business ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_health':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[2][0].text[-1] == '✅':
            markup.keyboard[2][0].text = 'Health'
            status = category_rm_msg
        else:
            markup.keyboard[2][0].text = 'Health ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
    
    elif call.data == 'cb_entertainment':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[2][1].text[-1] == '✅':
            markup.keyboard[2][1].text = 'Entertainment'
            status = category_rm_msg
        else:
            markup.keyboard[2][1].text = 'Entertainment ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
        
    elif call.data == 'cb_sci_tech':
        markup = call.message.reply_markup
        status = ''
        if markup.keyboard[3][0].text[-1] == '✅':
            markup.keyboard[3][0].text = 'Science & Tech'
            status = category_rm_msg
        else:
            markup.keyboard[3][0].text = 'Science & Tech ✅'
            status = category_add_msg
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    else:
        bot.answer_callback_query(call.id, 'Got the news!')

bot.polling(none_stop=True)