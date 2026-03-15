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

2. Если вам не нравится поведение участника, но формально он не нарушает правила, вы имеете право написать на него жалобу, предоставьте доказательства его плохого поведения и админ примет вашу жалобу, естественно если причина будет не весомая, или доказательств не будет, жалобу мы не примем, если участник получит 3 жалобы, его исключат навсегда без возможности вернуться, человек который кинул жалобу может отменить её.

3. Оᴄᴋᴏᴩбᴧᴇниᴇ ᴀдʍиниᴄᴛᴩᴀции и непослушание или игнорирование её.
Наказание ʙᴀᴩн на неделю, уважайте админов, они стараются и помогают вам. 
              
🤩{Рᴇᴋᴧᴀʍᴀ}🤩
1. Рᴇᴋᴧᴀʍᴀ в любом виде ɜᴀᴨᴩᴇщᴇна. Посторонние ссылки, просьбы подписаться на какие то тгк или просьбы проголосовать за вас в каких то батлах, это всё считается за нарушение и будет наказываться.
Наказание 2 варна навсегда

🤩{Пᴏʍᴏщь}🤩
1. Еᴄᴧи нᴇ ʍᴏжᴇᴛᴇ влиться во флуд то обᴩᴀᴛиᴛᴇᴄь ᴋ ʙᴧᴀдᴇᴧьцу или администратору, вам обязательно помогут.
2. Если у вас трудности с набором нормы вы так же можете попросить администрацию о помощи, не стесняйтесь, вам обязательно помогут.
4. Еᴄᴧи вы нᴇ ʍᴏжᴇᴛᴇ ᴀᴋᴛиʙиᴛь по какой либо причине, ᴨᴩᴇдуᴨᴩᴇдиᴛᴇ Вᴧадельца иᴧи ʙᴏɜьʍиᴛᴇ ᴩᴇᴄᴛ.
              
🤩{Нᴇᴀᴋᴛиʙ}🤩
1. Если вы Нᴇᴀᴋᴛиʙны во флуде 3-4 дня без причины или реста. Наказание варн навсегда.
2. Неактив больше 10 дней без причины или реста. Наказание кик. 

🤩{Спам}🤩
1. Сᴨᴀʍ ᴄᴛиᴋᴇᴩᴏʙ и ɸᴏᴛᴏ. Наказание ʙᴀᴩн навсегда.
2. Сᴨᴀʍ ᴄᴏᴏ 3 ᴏдинᴀᴋᴏʙых ᴄᴏᴏ. Наказание ʙᴀᴩн на неделю.
3. Сᴨᴀʍ буᴋʙ. Наказание ʙᴀᴩн на неделю.

🤩{Пᴏᴩнᴏᴦᴩᴀɸия}🤩
1. Пᴏᴩнᴏᴦᴩᴀɸия ɜᴀᴨᴩᴇщᴇна, это касается и расчленёнки и всего что может вызвать у участников отвращение, уважайте пожалуйста комфорт других участников. Наказание вы получите варн на 2 недели.

🤩{Ник}🤩
Изменяйте своë ник на свою роль +ник роль, за невыполнение наказание. Наказание варн 2 недели.

🤩{Неадекватное поведение}🤩
Если вы ведëте себя не прилично, администрация может вас забанить во флуде без шанса вернуться. Наказание: Бан.

🤩{Политика}🤩
Обсуждение политики запрещено. Воздержитесь от подобных тем во флуде — они могут быть неприятны части участников. Наказание: варн 2 недели.

Ps. Не знание правил не освобождает вас от ответственности.
"""

TEXTS = {
    'uk': {
        'welcome': "Вітаю! 👋\n\nУ цьому боті ви можете:\n✅ Ознайомитися з правилами\n✅ Переглянути вільні ролі та персонажів\n✅ Подати анкету на вступ до команди\n\n📰 Також ви можете читати свіжі новини та дивитись безкоштовні трансляції в тгк: @f1_racing_translation",
        'roles': "🎭 Ролі",
        'anketa': "📝 Подати анкету",
        'rules_btn': "📜 Правила",
        'news_btn': "🏎 Трансляції та новини",
        'news_msg': "🏁 Свіжі новини та безкоштовні трансляції Формули 1 доступні за посиланням:\n👉 @f1_racing_translation",
        'info': "F1 Flood\n--------------------------\nШАБЛОН АНКЕТИ:\n\n1. Повне ім'я бажаного персонажа.\n2. Ваш вік.\n--------------------------",
        'step1': "Крок 1: Введіть повне ім'я вашого персонажа:",
        'step2': "Крок 2: Введіть ваш вік:",
        'success': "✨ Вашу анкету успішно надіслано!",
        'admin_text': "НОВА АНКЕТА НА ВСТУП",
        'char': "Персонаж", 'user': "Користувач", 'age': "Вік",
        'accept': "✅ Схвалити", 'decline': "❌ Відхилити", 'review': "⏳ На розгляді"
    },
    'ru': {
        'welcome': "Привет! 👋\n\nВ этом боте вы можете:\n✅ Ознакомиться с правилами\n✅ Посмотреть свободные роли и персонажей\n✅ Подать анкету на вступление в команду\n\n📰 Также вы можете читать свежие новости и смотреть бесплатные трансляции в тгк: @f1_racing_translation",
        'roles': "🎭 Роли",
        'anketa': "📝 Подать анкету",
        'rules_btn': "📜 Правила",
        'news_btn': "🏎 Трансляции и новости",
        'news_msg': "🏁 Свежие новости и бесплатные трансляции Формулы 1 доступны по ссылке:\n👉 @f1_racing_translation",
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
    except Exception as e: print(f"Не вдалося видалити: {e}")

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
    markup.add(types.KeyboardButton(TEXTS[lang]['roles']), types.KeyboardButton(TEXTS[lang]['anketa']), types.KeyboardButton(TEXTS[lang]['rules_btn']), types.KeyboardButton(TEXTS[lang]['news_btn']))
    bot.send_message(call.message.chat.id, TEXTS[lang]['welcome'], reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['news_btn'], TEXTS['ru']['news_btn']])
def send_news(message):
    lang = user_lang.get(message.chat.id, 'uk')
    bot.send_message(message.chat.id, TEXTS[lang]['news_msg'])

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['rules_btn'], TEXTS['ru']['rules_btn']])
def send_rules(message):
    bot.send_message(message.chat.id, RULES_TEXT)

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['roles'], TEXTS['ru']['roles']])
def send_roles(message):
    try:
        bot.copy_message(message.chat.id, CHANNEL_ROLES_ID, 4)
    except Exception as e:
        bot.send_message(message.chat.id, "❌ Помилка: Не вдалося отримати ролі.")

@bot.message_handler(func=lambda message: message.text in [TEXTS['uk']['anketa'], TEXTS['ru']['anketa']])
def start_anketa(message):
    lang = user_lang.get(message.chat.id, 'uk')
    username = f"@{message.from_user.username}" if message.from_user.username else "Приховано"
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
    markup.add(types.InlineKeyboardButton(TEXTS[lang]['accept'], callback_data=f"accept_{user_id}"),
               types.InlineKeyboardButton(TEXTS[lang]['decline'], callback_data=f"decline_{user_id}"),
               types.InlineKeyboardButton(TEXTS[lang]['review'], callback_data=f"review_{user_id}"))
    admin_text = f"{TEXTS[lang]['admin_text']}\n--------------------------\n{TEXTS[lang]['char']}: {data['char_name']}\n{TEXTS[lang]['user']}: {data['username']}\n{TEXTS[lang]['age']}: {data['age']}\n--------------------------"
    bot.send_message(CHANNEL_ADMIN_ID, admin_text, reply_markup=markup)
    bot.send_message(user_id, TEXTS[lang]['success'])

@bot.callback_query_handler(func=lambda call: not call.data.startswith('lang_') and not call.data.startswith('reason_'))
def handle_admin_buttons(call):
    parts = call.data.split('_')
    action, target_user_id = parts[0], int(parts[1])
    if action == "accept":
        msg = "🎉 ВІТАЄМО! Вашу анкету СХВАЛЕНО. Посилання: https://t.me/+bnvTpMG_lyhlZDky\n⚠️ Видалиться через 10 хвилин."
        sent = bot.send_message(target_user_id, msg)
        threading.Thread(target=delete_msg_after_delay, args=(target_user_id, sent.message_id, 600)).start()
        bot.edit_message_text(f"{call.message.text}\n\n📢 СТАТУС: СХВАЛЕНО ✅", CHANNEL_ADMIN_ID, call.message.message_id)
    elif action == "decline":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("❌ Не підходить вік", callback_data=f"reason_age_{target_user_id}_{call.message.message_id}"),
            types.InlineKeyboardButton("❌ Роль вже зайнята", callback_data=f"reason_taken_{target_user_id}_{call.message.message_id}"),
            types.InlineKeyboardButton("❌ Напишу в особисті", callback_data=f"reason_dm_{target_user_id}_{call.message.message_id}")
        )
        bot.send_message(CHANNEL_ADMIN_ID, "📝 Оберіть причину відхилення:", reply_markup=markup)
    elif action == "review":
        bot.send_message(target_user_id, "⏳ Ваша анкета НА РОЗГЛЯДІ.")
        bot.edit_message_text(f"{call.message.text}\n\n📢 СТАТУС: РОЗГЛЯД ⏳", CHANNEL_ADMIN_ID, call.message.message_id, reply_markup=call.message.reply_markup)
    bot.answer_callback_query(call.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('reason_'))
def handle_reasons(call):
    _, reason_type, target_user_id, admin_msg_id = call.data.split('_')
    target_user_id, admin_msg_id = int(target_user_id), int(admin_msg_id)
    reasons = {"age": "Не підходить вік.", "taken": "Роль вже зайнята.", "dm": "Зверніться до адміністратора в особисті."}
    reason_text = reasons.get(reason_type)
    bot.send_message(target_user_id, f"😔 Вашу анкету було ВІДХИЛЕНО.\n\n⚠️ Причина: {reason_text}")
    msg = bot.get_message(CHANNEL_ADMIN_ID, admin_msg_id)
    bot.edit_message_text(f"{msg.text}\n\n📢 СТАТУС: ВІДХИЛЕНО ❌\nПричина: {reason_text}", CHANNEL_ADMIN_ID, admin_msg_id)
    bot.answer_callback_query(call.id, text="Причину надіслано")
    bot.delete_message(CHANNEL_ADMIN_ID, call.message.message_id)

bot.polling(none_stop=True)
