import wikipediaapi
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext, MessageHandler, filters, ConversationHandler

import threading
import asyncio

from collections import defaultdict
from datetime import datetime, timedelta

user_languages = {}

index_lang = 0

connected_users = {}
active_users = {}

counter = 1
counter_active = 1

current_id = 0

flag = -1
flag_active = -1

can_search = False

user_last_message_time = defaultdict(lambda: datetime.now())
tasks = {}

forbidden_symbols = "!@\"\'#№$~`:;[]{}/\\|?.,<>()*&^%-_=+"
allowed_characters = [ ["абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "", "0123456789"], # 0 - Русский
                           ["abcdefghijklmnopqrstuvwxyz", "", "0123456789"] ]   # 1 - English
allowed_characters[0][1] = allowed_characters[0][0].upper()
allowed_characters[1][1] = allowed_characters[1][0].upper()

bot_token = "BOT_TOKEN"

async def send_delayed_message(chat_id: int):
    global counter_active
    await asyncio.sleep(16)
    if datetime.now() - user_last_message_time[chat_id] >= timedelta(seconds=15):
        for i in range(len(active_users)): # active_users.pop(active_users.index(chat_id))
            if active_users[i] == chat_id: # counter_active -= 1
                active_users.pop(i)
                counter_active -= 1
        

async def start(update: Update, context: CallbackContext) -> None:
    global counter
    global counter_active
    global flag
    global flag_active
    global can_search
    can_search = False
    chat_id = update.message.chat_id
    user_last_message_time[chat_id] = datetime.now()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    if chat_id in tasks:
        tasks[chat_id].cancel()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    user = update.message.from_user
    user_info = (
        f"User ID: {user.id}\n"
        f"Username: {user.username}\n"
        f"Full Name: {user.full_name}\n"
        f"Language Code: {user.language_code}"
    )
    for i in range(len(connected_users)):
        if connected_users[i] == user.id:
            flag = i
            break
    for i in range(len(active_users)):
        if active_users[i] == user.id:
            flag_active = i
            break
    if flag_active == -1:
        active_users[counter_active - 1] = user.id
        counter_active += 1
    flag_active = -1
    if flag == -1:
        print(counter, ". Successful connection", sep = "")
        connected_users[counter - 1] = user.id
        counter += 1
    else:
        print("\nUser with ID:", connected_users[flag], "successfully reconnected")
        flag = -1
    print(user_info)
    await update.message.reply_text('Привет! Я бот, который поможет найти значение любого слова в Википедии! Только сначала выбери язык при помощи команды /language\n\nHello! I\'m a bot that will help you find the meaning of any word on Wikipedia! Just first select the language using the /language command')

async def language(update: Update, context: CallbackContext) -> None:
    global can_search
    global counter
    global counter_active
    global flag
    global flag_active
    can_search = False
    chat_id = update.message.chat_id
    user_last_message_time[chat_id] = datetime.now()
    if chat_id in tasks:
        tasks[chat_id].cancel()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    user = update.message.from_user
    for i in range(len(active_users)):
        if active_users[i] == user.id:
            flag_active = i
            break
    if flag_active == -1:
        active_users[counter_active - 1] = user.id
        counter_active += 1
    flag_active = -1
    for i in range(len(connected_users)):
        if connected_users[i] == user.id:
            flag = i
            break
    if flag == -1:
        connected_users[counter - 1] = user.id
        counter += 1
    else:
        flag = -1
    print("\nUser with ID", user.id, "choosing language")
    #print(user_info)
    keyboard = [
        [KeyboardButton("Русский"), KeyboardButton("English")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text('Выберите язык Википедии / Choose a language Wiki:', reply_markup=reply_markup)


async def language_choice(update: Update, context: CallbackContext) -> None:
    global index_lang
    global counter_active
    global flag_active
    chat_id = update.message.chat_id
    text = update.message.text
    user = update.message.from_user
    user_last_message_time[chat_id] = datetime.now()
    for i in range(len(active_users)):
        if active_users[i] == user.id:
            flag_active = i
            break
    if flag_active == -1:
        active_users[counter_active - 1] = user.id
        counter_active += 1
    flag_active = -1
    if text == "Русский":
        index_lang = 0
        user_languages[chat_id] = 'ru'
        if chat_id in tasks:
            tasks[chat_id].cancel()
        tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
        await update.message.reply_text('Вы выбрали русский язык. Напишите /search <ваше слово> для поиска (или /search для ввода слова для поиска следующим сообщением).', reply_markup=ReplyKeyboardRemove())
    elif text == "English":
        index_lang = 1
        user_languages[chat_id] = 'en'
        if chat_id in tasks:
            tasks[chat_id].cancel()
        tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
        await update.message.reply_text('You have selected English. Type /search <your word> to search (or /search to input word for search in next message).', reply_markup=ReplyKeyboardRemove())

def get_first_paragraph(summary: str) -> str:
    return summary.split('\n')[0]

async def search(update: Update, context: CallbackContext) -> None:
    global current_id
    global can_search
    global counter_active
    global flag_active
    chat_id = update.message.chat_id
    user = update.message.from_user
    user_last_message_time[chat_id] = datetime.now()
    for i in range(len(active_users)):
        if active_users[i] == user.id:
            flag_active = i
            break
    if flag_active == -1:
        active_users[counter_active - 1] = user.id
        counter_active += 1
    flag_active = -1
    if chat_id in tasks:
        tasks[chat_id].cancel()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    query = ' '.join(context.args)
    if chat_id not in user_languages:
        await update.message.reply_text('Пожалуйста, сначала выберите язык с помощью /language \n\n Please select a language first using /language.')
        return ConversationHandler.END
    
    can_search = True
    await choose_word(update, context, query)

async def choose_word(update: Update, context: CallbackContext, query: str) -> None:
    global current_id
    global counter_active
    global flag_active
    chat_id = update.message.chat_id
    user = update.message.from_user
    user_last_message_time[chat_id] = datetime.now()
    for i in range(len(active_users)):
        if active_users[i] == user.id:
            flag_active = i
            break
    if flag_active == -1:
        active_users[counter_active - 1] = user.id
        counter_active += 1
    flag_active = -1
    if chat_id in tasks:
        tasks[chat_id].cancel()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    if chat_id not in user_languages:
        await update.message.reply_text('Пожалуйста, сначала выберите язык с помощью /language \n\n Please select a language first using /language.')
        return

    wiki = wikipediaapi.Wikipedia(language=user_languages[chat_id], user_agent='YourAppName/1.0 (yourname@example.com)')

    if not query:
        if index_lang == 0:
            await update.message.reply_text('Введите слово для поиска :)')
        elif index_lang == 1:
            await update.message.reply_text('Input word to search :D')
        return

    # for index in query:
    #     for i in range(len(forbidden_symbols)):
    #         if index == forbidden_symbols[i]:
    #             if index_lang == 0:
    #                 st = 'Слово содержит недопустимый символ: ' + index
    #                 await update.message.reply_text(st)
    #             elif index_lang == 1:
    #                 st = 'The word contains an invalid character: ' + index
    #                 await update.message.reply_text(st)
    #             return
    all_characters_right = True #dont work!!!!!!!!!!!!
    for index in query:
        character_right = False
        for syms in allowed_characters[index_lang]:
            for sym in syms:
                if index == sym:
                    character_right = True
        if character_right == False:
            all_characters_right = False
            break
    if all_characters_right == False:
        if index_lang == 0:
            st = 'Слово содержит недопустимый символ: ' + index
            await update.message.reply_text(st)
        elif index_lang == 1:
            st = 'The word contains an invalid character: ' + index
            await update.message.reply_text(st)
        return

    all_pos_var_of_word = [query, query.lower(), query.upper(), query[0].upper() + query[1:].lower()]
    find = False
    page = wiki.page(query)
    user = update.message.from_user
    user_info = (f"User ID: {user.id}\n")
    if can_search == True:
        for word in all_pos_var_of_word:
            if find == True:
                break
            page = wiki.page(word)
            if page.exists():
                find = True
                if current_id != user.id:
                    current_id = user.id
                    print("\n", user_info, end = "")
                print("Searching '", query, "' (modify ", word, ") : Successful\n", sep = "")
                first_paragraph = get_first_paragraph(page.summary)
                await update.message.reply_text(first_paragraph)
        if find == False:
            if current_id != user.id:
               current_id = user.id
               print("\n", user_info, end = "")
            print("Searching '", query, "': Failed\nIn all Variations: ", all_pos_var_of_word, "\n", sep = "")
            await update.message.reply_text('Page not found.')
    else:
        if index_lang == 0:
            await update.message.reply_text('Надо использовать команду /search для поиска.')
        elif index_lang == 1:
            await update.message.reply_text('You need to use command /search at first.')

async def qwerty(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    user_last_message_time[chat_id] = datetime.now()
    if chat_id in tasks:
        tasks[chat_id].cancel()
    tasks[chat_id] = asyncio.create_task(send_delayed_message(chat_id))
    query = update.message.text
    await choose_word(update, context, query)

def terminal_input_listener(loop):
    while True:
        user_input = input()
        if user_input.strip().lower() == "exit":
            print("Exiting...")
            for task in tasks.values():
                task.cancel()
            for i in range(len(active_users)):
                loop.call_soon_threadsafe(loop.create_task, notify_all_users(i))
            loop.call_soon_threadsafe(loop.stop)
            break
   
async def notify_all_users(index) -> int:
    bot = Bot(token=bot_token)
    print(f"Message sent to user with ID", active_users[index])
    try:
        if index_lang == 0:
            await bot.send_message(chat_id=active_users[index], text="Бот остановлен администратором. Повторите попытку позже :(")
        elif index_lang == 1:
            await bot.send_message(chat_id=active_users[index], text="Bot stopped by administrator. Try again later D:")
    except Exception as e:
        print(f"Failed to send message to {active_users[index]}: {e}")
        

def main():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    application = ApplicationBuilder().token(bot_token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("language", language))
    application.add_handler(CommandHandler("search", search))
    application.add_handler(MessageHandler(filters.Regex('^(Русский|English)$'), language_choice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, qwerty))

    input_thread = threading.Thread(target=terminal_input_listener, args=(loop,), daemon=True)
    input_thread.start()

    print("System started. Ready for connections.")
    application.run_polling()

if __name__ == '__main__':
    main()
