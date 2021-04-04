import psycopg2
from consts import *
from api_data import username, api_id, api_hash
from classifier import get_en_news_category, get_ru_news_category
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.custom import Button
from telethon import events, TelegramClient
from contextlib import closing

client = TelegramClient(username, api_id, api_hash).start()
bot = TelegramClient('CoolStoryBot', api_id, api_hash).start(bot_token=API_TOKEN)

@client.on(events.NewMessage(chats=[BBC_ID]))
async def news_handler(event):
    await client.forward_messages(BOT_ID, event.message)

# Categories keyboard generation
def create_keyboard(chat_id):
    btns = {'Спорт'           : 'Sport',
            'Мир'             : 'World',
            'Россия'          : 'US',
            'Бизнес'          : 'Business',
            'Интернет и СМИ'  : 'Health',
            'Культура'        : 'Entertainment',
            'Наука и техника' : 'Science & Tech'}
    
    user_entry = []
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT * FROM bot_user WHERE chat_id = {chat_id}')
            user_entry = cursor.fetchall()

    layout = [value for value in btns.values()] if user_entry[0][8] else [key for key in btns.keys()]
    for i in range(0, 7):
        if user_entry[0][i]==True:
            layout[i] += ' ✅'

    if not user_entry[0][9]:
            layout[2] = 'Россия ✅' if user_entry[0][7] else 'Россия'
            layout[4] = 'Интернет и СМИ ✅' if user_entry[0][7] else 'Интернет и СМИ'

    callbacks = ['cb_us', 'cb_health'] if user_entry[0][9] else ['cb_ru', 'cb_internet']
    lang_btn = 'Switch to Russian' if user_entry[0][9] else 'Сменить на английский'

    keyboard = [
        [Button.inline(layout[0], 'cb_sport'), Button.inline(layout[1], 'cb_world')],
        [Button.inline(layout[2], callbacks[0]), Button.inline(layout[3], 'cb_business')],
        [Button.inline(layout[4], callbacks[1]), Button.inline(layout[5], 'cb_entertainment')],
        [Button.inline(layout[6], 'cb_sci_tech')],
        [Button.inline(lang_btn, 'cb_lang')]
    ]
    return keyboard

# Handle '/start' 
@bot.on(events.NewMessage(pattern='/start'))
async def send_welcome(event):
    en_welcome = "Hello! I'm CoolstoryBot. What kind of news would you like to receive?"
    ru_welcome = "Привет! Я КулСториБот. Какие новости ты хочешь получать?"
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT * FROM bot_user WHERE chat_id = {event.chat_id}')
            user_entry = cursor.fetchall()
            if len(user_entry)==0:
                cursor.execute(f'INSERT INTO bot_user(sport, world, us, business, health, entertainment, sci_tech, ru, internet, lang, chat_id)\
                VALUES (FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, {event.chat_id},)')
                await bot.send_message(event.chat_id, ru_welcome, buttons=create_keyboard(event.chat_id))
            else:
                if user_entry[0][9]:
                    await bot.send_message(event.chat_id, en_welcome, buttons=create_keyboard(event.chat_id))
                else:
                    await bot.send_message(event.chat_id, ru_welcome, buttons=create_keyboard(event.chat_id))

# Handle '/categories'
@bot.on(events.NewMessage(pattern='/categories'))
async def send_categories(event):
    await bot.send_message(event.chat_id, 'Here are the categories:', buttons=create_keyboard(event.chat_id))

# Handle incoming news 
@bot.on(events.NewMessage(chats=[CLIENT_ID]))
async def client_handler(event):
    from_id = event.message.fwd_from.from_id
    msg = event.message.message.text.split('\n')[0]

    if from_id==BBC_ID:
        ctg = get_en_news_category(msg) 
    elif from_id==MEDUZA_ID:
        ctg = get_ru_news_category(msg)

    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True
            cursor.execute(f'SELECT chat_id FROM bot_user WHERE {ctg} = TRUE')
            sub_users = cursor.fetchall()
            for user in sub_users:
                await bot.forward_messages(user[0], event.message)


# Handle button clicks
@bot.on(events.CallbackQuery)
async def keyboard_handler(event):
    with closing(psycopg2.connect(dbname=DB_NAME, user=USER, password=PASS, host=HOST)) as conn:
        with conn.cursor() as cursor:
            conn.autocommit = True

            btns = [b'cb_sport', b'cb_world', b'cb_us', b'cb_business', b'cb_health', 
                    b'cb_entertainment', b'cb_sci_tech', b'cb_ru', b'cb_internet']
            pos = 0
            for key in btns:
                if event.data == key:
                    key = key.decode('UTF-8')
                    msg    = await event.get_message()
                    markup = msg.reply_markup
                    status = ''
                    curr_btn = markup.rows[pos//2].buttons[pos%2].text
                    if curr_btn[-1] == '✅':
                        markup.rows[pos//2].buttons[pos%2].text = curr_btn[:-2]
                        status = CATEGORY_RM_MSG
                        cursor.execute(f'UPDATE bot_user SET {key[3:]} = FALSE WHERE chat_id = {event.chat_id}')
                    else:
                        markup.rows[pos//2].buttons[pos%2].text = f'{curr_btn} ✅'
                        status = CATEGORY_ADD_MSG
                        cursor.execute(f'UPDATE bot_user SET {key[3:]} = TRUE WHERE chat_id = {event.chat_id}')
                    
                    await msg.edit(buttons=markup)

                    await event.answer(status)
                    break
                pos += 1 
            if pos >= 7:
                btn_text = markup.rows[4].buttons[0].text
                lang = 'TRUE' if btn_text=='Сменить на английский' else 'FALSE'
                cursor.execute(f'UPDATE bot_user SET lang = {lang} WHERE chat_id = {event.chat_id}')
                await msg.edit(buttons=create_keyboard(event.chat_id))

client.run_until_disconnected()
bot.run_until_disconnected()        