import telebot
from telebot import types
import time
import threading

TOKEN = '8338826510:AAE4NaY5KAowuT5o6yD_iWj96oTA0JFXBAs'
CHANNEL_ROLES_ID = -1003547370132
CHANNEL_ADMIN_ID = -1003606148765

bot = telebot.TeleBot(TOKEN)
user_steps = {}
user_lang = {}

RULES_TEXT = """
🤩🤩🤩🤩🤩🤩🤩
🤩{Оᴄᴋᴏᴩбᴧᴇния}🤩
1. Даже если вы оскорбили участника с целью просто пошутить, надо видеть границы, если участнику стало обидно от ваших слов вы получаете варн навсегда.
Также если участник пошутил что ему обидно , то тот участник тоже получает варн на всегда. 
Наказание варн навсегда

2. Если вам не нравится поведение участника, но формально он не нарушает правила, вы имеете право написать на него жалобу, предоставьте доказательства его плохого поведения и админ примет вашу жалобу.
Если участник получит 3 жалобы, его исключат навсегда.

3. Оᴄᴋᴏᴩбᴧᴇниᴇ ᴀдʍиниᴄᴛᴩᴀции и непослушание или игнорирование её.
Наказание ʙᴀᴩн на неделю.

🤩{Рᴇᴋᴧᴀʍᴀ}🤩
Рᴇᴋᴧᴀʍᴀ в любом виде ɜᴀᴨᴩᴇщᴇна. Посторонние ссылки, просьбы подписаться - Наказание 2 варна навсегда.

🤩{Пᴏʍᴏщь}🤩
Если не можете влиться во флуд или есть трудности с набором нормы — обратитесь к администрации. Если не можете активить — предупредите владельца или возьмите рест.

🤩{Нᴇᴀᴋᴛиʙ}🤩
1. Неактив 3-4 дня без причины — варн навсегда.
2. Неактив больше 10 дней — кик.

🤩{Спам}🤩
1. Спам стикеров/фото — варн навсегда.
2. Спам одинаковых сообщений — варн на неделю.
3. Спам букв — варн на неделю.

🤩{Пᴏᴩнᴏᴦᴩᴀɸия}🤩
Запрещена, включая расчленёнку. Наказание — варн на 2 недели.

🤩{Ник}🤩
Изменяйте ник на роль + ник. Наказание — варн 2 недели.

🤩{Неадекватное поведение}🤩
Бан без шанса вернуться.

🤩{Политика}🤩
Обсуждение политики запрещено. Наказание — варн 2 недели.

Ps. Не знание правил не освобождает вас от ответственности.
"""

TEXTS = {
    'uk': {
        'welcome': "Вітаємо! Тут ви можете ознайомитися з правилами, переглянути вільні ролі та подати заявку.",
        'roles': "🎭 Ролі",
        'anketa': "📝 Подати анкету",
        'rules_btn': "📜 Правила",
        'info': "F1 Flood\n--------------------------\nШАБЛОН АНКЕТИ:\n\n1. Повне ім'я бажаного персонажа.\n2. Ваш вік.\n--------------------------",
        'step1': "Крок 1: Введіть повне ім'я вашого персонажа:",
        'step2': "Крок 2: Введіть ваш вік:",
        'success': "✨ Вашу анкету успішно надіслано!",
        'admin_text': "НОВА АНКЕТА НА ВСТУП",
        'char': "Персонаж", 'user': "Користувач", 'age': "Вік",
        'accept': "✅ Схвалити", 'decline': "❌ Відхилити", 'review': "⏳ На розгляді"
    },
    'ru': {
        'welcome': "Приветствуем! Здесь вы можете ознакомиться с правилами, посмотреть свободные роли и подать заявку.",
        'roles': "🎭 Роли",
        'anketa': "📝 Подать анкету",
        'rules_btn': "📜 Правила",
        'info': "F1 Flood\n--------------------------\nШАБЛОН АНКЕТЫ:\n\n1. Полное имя желаемого персонажа.\n2. Ваш возраст.\n--------------------------",
        'step1': "Шаг 1: Введите полное имя вашего персонажа:",
        'step2': "Шаг 2: Введите ваш возраст:",
        'success': "✨ Ваша анкета успешно отправлена!",
        'admin_text': "НОВАЯ АНКЕТА НА ВСТУПЛЕНИЕ",
        'char': "Персонаж", 'user': "Пользователь", 'age': "Возраст",
        'accept': "✅ Одобрить", 'decline': "❌ Отклонить", 'review': "⏳ На рассмотрении"
    }
}

def delete_msg_after_delay(chat_id, message_id, delay=600):
    time.sleep(delay)
    try: bot.delete_message(chat_id, message_id)
    except: pass

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
    markup.add(types.KeyboardButton(TEXTS[lang]['roles']), types.KeyboardButton(TEXTS[lang]['anketa']), types.KeyboardButton(TEXTS[lang]['rules_btn']))
    bot.send_message(call.message.chat.id, TEXTS[lang]['welcome'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['rules_btn'], TEXTS['ru']['rules_btn']])
def send_rules(message):
    bot.send_message(message.chat.id, RULES_TEXT)

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['roles'], TEXTS['ru']['roles']])
def send_roles(message):
    try:
        updates = bot.get_updates()
        # Бот бере останнє повідомлення з історії каналу (потрібні права адміністратора в каналі)
        messages = bot.get_chat_history(CHANNEL_ROLES_ID, limit=1)
        if messages:
            bot.copy_message(message.chat.id, CHANNEL_ROLES_ID, messages[0].id)
        else:
            bot.send_message(message.chat.id, "❌ Повідомлень не знайдено.")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Помилка: {e}")

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['anketa'], TEXTS['ru']['anketa']])
def start_anketa(message):
    lang = user_lang.get(message.chat.id, 'uk')
    bot.send_message(message.chat.id, "💡 Нагадування: Вільні ролі та правила доступні в головному меню.")
    user_steps[message.chat.id] = {'username': f"@{message.from_user.username}" if message.from_user.username else "Приховано"}
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
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['accept'], callback_data=f"accept_{user_id}"),
               types.InlineKeyboardButton(TEXTS[lang]['decline'], callback_data=f"decline_{user_id}"),
               types.InlineKeyboardButton(TEXTS[lang]['review'], callback_data=f"review_{user_id}"))
    admin_text = f"{TEXTS[lang]['admin_text']}\n--------------------------\n{TEXTS[lang]['char']}: {data['char_name']}\n{TEXTS[lang]['user']}: {data['username']}\n{TEXTS[lang]['age']}: {data['age']}\n--------------------------"
    bot.send_message(CHANNEL_ADMIN_ID, admin_text, reply_markup=markup)
    bot.send_message(user_id, TEXTS[lang]['success'])

@bot.callback_query_handler(func=lambda call: not call.data.startswith('lang_'))
def handle_admin_buttons(call):
    parts = call.data.split('_')
    action, target_user_id = parts[0], int(parts[1])
    if action == "accept":
        msg = "🎉 ВІТАЄМО! Вашу анкету СХВАЛЕНО. Посилання: https://t.me/+bnvTpMG_lyhlZDky\n⚠️ Повідомлення видалиться через 10 хвилин."
        sent = bot.send_message(target_user_id, msg)
        threading.Thread(target=delete_msg_after_delay, args=(target_user_id, sent.message_id)).start()
    elif action == "decline": bot.send_message(target_user_id, "😔 Вашу анкету було ВІДХИЛЕНО.")
    elif action == "review": bot.send_message(target_user_id, "⏳ Ваша анкета НА РОЗГЛЯДІ.")
    bot.edit_message_text(f"{call.message.text}\n\n📢 СТАТУС: {action.upper()}", CHANNEL_ADMIN_ID, call.message.message_id)

bot.polling(none_stop=True)
