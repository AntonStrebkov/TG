import csv
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler


bot_token = ''
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Привет!\nЯ Бот-справочник! Напиши команду, '
                                                       'которую мне необходимо выполнить:\n'
                                                       '/read - показать весь справочник\n'
                                                       '/add - добавить запись\n'
                                                       '/delete - удалить запись\n'
                                                       'Успехов!')
def read_info():
    with open('phonebook.csv', encoding='utf-8') as f:
        full_file = csv.reader(f, delimiter=';')
        res = list(full_file)
        return res
def read(update, context):
    context.bot.send_message(update.effective_chat.id, read_info())

def add(update, context):
    context.bot.send_message(update.effective_chat.id, )

def delete(update, context):
    context.bot.send_message(update.effective_chat.id, )


start_handler = CommandHandler('start', start)
add_handler = CommandHandler('add', add)
delete_handler = CommandHandler('delete', delete)
read_handler = CommandHandler('read', read)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(read_handler)
updater.start_polling()
updater.idle()