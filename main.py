import telebot
from telebot import types
import time
import threading

TOKEN = '8338826510:AAE4NaY5KAowuT5o6yD_iWj96oTA0JFXBAs'
CHANNEL_ROLES_ID = -1003547370132
CHANNEL_ADMIN_ID = -1003606148765
ROLE_MESSAGE_ID = 2

bot = telebot.TeleBot(TOKEN)
user_steps = {}
user_lang = {}

# Словник з текстами
TEXTS = {
    'uk': {
        'welcome': "Вітаємо у нашому боті!\n\nТут ви можете ознайомитися з правилами та подати заявку на вступ.",
        'roles': "🎭 Ролі",
        'anketa': "📝 Подати анкету",
        'info': "F1 Flood\n--------------------------\nШАБЛОН АНКЕТИ:\n\n1. Повне ім'я бажаного персонажа.\n2. Ваш вік.\n--------------------------",
        'step1': "Крок 1: Введіть повне ім'я вашого персонажа:",
        'step2': "Крок 2: Введіть ваш вік:",
        'success': "✨ Вашу анкету успішно надіслано!",
        'admin_text': "НОВА АНКЕТА НА ВСТУП",
        'char': "Персонаж",
        'user': "Користувач",
        'age': "Вік",
        'accept': "✅ Схвалити",
        'decline': "❌ Відхилити",
        'review': "⏳ На розгляді"
    },
    'ru': {
        'welcome': "Приветствуем в нашем боте!\n\nЗдесь вы можете ознакомиться с правилами и подать заявку на вступление.",
        'roles': "🎭 Роли",
        'anketa': "📝 Подать анкету",
        'info': "F1 Flood\n--------------------------\nШАБЛОН АНКЕТЫ:\n\n1. Полное имя желаемого персонажа.\n2. Ваш возраст.\n--------------------------",
        'step1': "Шаг 1: Введите полное имя вашего персонажа:",
        'step2': "Шаг 2: Введите ваш возраст:",
        'success': "✨ Ваша анкета успешно отправлена!",
        'admin_text': "НОВАЯ АНКЕТА НА ВСТУПЛЕНИЕ",
        'char': "Персонаж",
        'user': "Пользователь",
        'age': "Возраст",
        'accept': "✅ Одобрить",
        'decline': "❌ Отклонить",
        'review': "⏳ На рассмотрении"
    }
}

def delete_msg_after_delay(chat_id, message_id, delay=10):
    time.sleep(delay)
    try: bot.delete_message(chat_id, message_id)
    except Exception as e: print(f"Не вдалося видалити повідомлення: {e}")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk"),
               types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"))
    bot.send_message(message.chat.id, "Виберіть мову / Выберите язык:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def set_language(call):
    lang = call.data.split('_')[1]
    user_lang[call.message.chat.id] = lang
    bot.delete_message(call.message.chat.id, call.message.message_id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton(TEXTS[lang]['roles']), types.KeyboardButton(TEXTS[lang]['anketa']))
    bot.send_message(call.message.chat.id, TEXTS[lang]['welcome'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['roles'], TEXTS['ru']['roles']])
def send_roles(message):
    try: bot.copy_message(message.chat.id, CHANNEL_ROLES_ID, ROLE_MESSAGE_ID)
    except Exception as e: bot.send_message(message.chat.id, "❌ Помилка/Ошибка.")

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['anketa'], TEXTS['ru']['anketa']])
def start_anketa(message):
    lang = user_lang.get(message.chat.id, 'uk')
    username = f"@{message.from_user.username}" if message.from_user.username else "Приховано/Скрыто"
    user_steps[message.chat.id] = {'username': username}
    bot.send_message(message.chat.id, TEXTS[lang]['info'])
    bot.send_message(message.chat.id, TEXTS[lang]['step1'])
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    lang = user_lang.get(message.chat.id, 'uk')
    user_steps[message.chat.id]['char_name'] = message.text
    bot.send_message(message.chat.id, TEXTS[lang]['step2'])
    bot.register_next_step_handler(message, process_age)

def process_age(message):
    lang = user_lang.get(message.chat.id, 'uk')
    user_id = message.chat.id
    user_steps[user_id]['age'] = message.text
    data = user_steps[user_id]
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(TEXTS[lang]['accept'], callback_data=f"accept_{user_id}"),
        types.InlineKeyboardButton(TEXTS[lang]['decline'], callback_data=f"decline_{user_id}"),
        types.InlineKeyboardButton(TEXTS[lang]['review'], callback_data=f"review_{user_id}")
    )
    admin_text = f"{TEXTS[lang]['admin_text']}\n--------------------------\n{TEXTS[lang]['char']}: {data['char_name']}\n{TEXTS[lang]['user']}: {data['username']}\n{TEXTS[lang]['age']}: {data['age']}\n--------------------------"
    bot.send_message(CHANNEL_ADMIN_ID, admin_text, reply_markup=markup)
    bot.send_message(user_id, TEXTS[lang]['success'])



@bot.callback_query_handler(func=lambda call: not call.data.startswith('lang_'))
def handle_admin_buttons(call):
    parts = call.data.split('_')
    action, target_user_id = parts[0], int(parts[1])
    
    if action == "accept":
        msg = "🎉 ВІТАЄМО! Вашу анкету СХВАЛЕНО. Посилання: https://t.me/+bnvTpMG_lyhlZDky\n⚠️ Видалиться через 10 хвилин."
        sent = bot.send_message(target_user_id, msg)
        threading.Thread(target=delete_msg_after_delay, args=(target_user_id, sent.message_id, 600)).start()
    elif action == "decline":
        bot.send_message(target_user_id, "😔 Вашу анкету було ВІДХИЛЕНО.")
    elif action == "review":
        bot.send_message(target_user_id, "⏳ Ваша анкета НА РОЗГЛЯДІ.")
    
    bot.edit_message_text(f"{call.message.text}\n\n📢 СТАТУС: {action.upper()}", CHANNEL_ADMIN_ID, call.message.message_id, reply_markup=call.message.reply_markup if action == "review" else None)
    bot.answer_callback_query(call.id, text=f"Статус: {action}")

bot.polling(none_stop=True)