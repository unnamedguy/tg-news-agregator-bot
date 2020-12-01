import telebot

API_TOKEN = '1436454776:AAGlRrnESJA4ih1yGia4fGy9EcsIwsIqB3w'

bot = telebot.TeleBot(API_TOKEN)


# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Привет, я КулсториБот. Могу рассказать тебе удивительные истории на выбранную тему!\
""")


keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Tec', '')
keyboard1.row('', '')
keyboard1.row('', '')



@bot.message_handler(commands=['news', 'start'])
def start_message2(message):
    bot.send_message(message.chat.id, 'лол кек', reply_markup=keyboard1)


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
#@bot.message_handler(func=lambda message: True)
@bot.message_handler(content_types=['text'])
def echo_message(message):
    if message.text == 'Tec':
        keyboard1.keyboard[0][0] = 'Tec ✅'
        bot.send_message(message.chat.id, "Вывел новости технологий")      
        bot.send_message(message.chat.id, 'Категория добавлена', reply_markup=keyboard1)
    #else if
    #bot.send_message(message.chat.id, message.text + "\nДержу в курсе!")

bot.polling()