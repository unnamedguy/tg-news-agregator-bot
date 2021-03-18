import telebot
from Classifier import getEnNewsCategory
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '1436454776:AAGlRrnESJA4ih1yGia4fGy9EcsIwsIqB3w'

bot = telebot.TeleBot(API_TOKEN)

# Handle '/start' 
# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """Привет, я КулсториБот. Могу рассказать
тебе удивительные истории на выбранную тему""", reply_markup=gen_markup())

# Handle '/help'
# Commands list
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, '\n/start\n/change\n/help') 

# Keyboard generation
def gen_markup():
    markup = InlineKeyboardMarkup()
    #markup.row_width = 2
    markup.row(InlineKeyboardButton("Общество", callback_data="cb_society"),
                InlineKeyboardButton("Наука", callback_data="cb_science"))
    markup.row(InlineKeyboardButton("Спорт", callback_data="cb_sport"),
                InlineKeyboardButton("Развлечения", callback_data="cb_entertainment"))
    markup.row(InlineKeyboardButton("Экономика", callback_data="cb_economy"),
                InlineKeyboardButton("Технологии", callback_data="cb_technology"))
    markup.add(InlineKeyboardButton("Другое", callback_data="cb_other"))
    markup.add(InlineKeyboardButton("Получить новости", callback_data="cb_getnews"))
    return markup

# Creates keyboard on click
@bot.message_handler(commands=['change'])
def start_message2(message):
    bot.send_message(message.chat.id, 'Категории:', reply_markup=gen_markup())

# Handles buttons' clicks
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'cb_society':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[0][0].text[-1] == '✅':
            markup.keyboard[0][0].text = 'Общество'
            status = "Категория удалена!"
        else:
            markup.keyboard[0][0].text = 'Общество ✅'
            status = "Категория добавлена!"
            
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)    

    elif call.data == 'cb_science':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[0][1].text[-1] == '✅':
            markup.keyboard[0][1].text = 'Наука'
            status = "Категория удалена!"
        else:
            markup.keyboard[0][1].text = 'Наука ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_sport':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[1][0].text[-1] == '✅':
            markup.keyboard[1][0].text = 'Спорт'
            status = "Категория удалена!"
        else:
            markup.keyboard[1][0].text = 'Спорт ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)

    elif call.data == 'cb_entertainment':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[1][1].text[-1] == '✅':
            markup.keyboard[1][1].text = 'Развлечения'
            status = "Категория удалена!"
        else:
            markup.keyboard[1][1].text = 'Развлечения ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    elif call.data == 'cb_economy':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[2][0].text[-1] == '✅':
            markup.keyboard[2][0].text = 'Экономика'
            status = "Категория удалена!"
        else:
            markup.keyboard[2][0].text = 'Экономика ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
    
    elif call.data == 'cb_technology':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[2][1].text[-1] == '✅':
            markup.keyboard[2][1].text = 'Технологии'
            status = "Категория удалена!"
        else:
            markup.keyboard[2][1].text = 'Технологии ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  
        
    elif call.data == 'cb_other':
        markup = call.message.reply_markup
        status = ""
        if markup.keyboard[3][0].text[-1] == '✅':
            markup.keyboard[3][0].text = 'Другое'
            status = "Категория удалена!"
        else:
            markup.keyboard[3][0].text = 'Другое ✅'
            status = "Категория добавлена!"
        bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.id, 
            reply_markup=markup)
        bot.answer_callback_query(call.id, status)  

    else:
        bot.answer_callback_query(call.id, 'Получили новости!\nДержу в курсе!')

bot.polling(none_stop=True)