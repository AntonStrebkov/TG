import logging
import random

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

reply_keyboard = [['/info', '/play', '/close']]
stop_keyboard = [['/stop']]

markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
stop_markup = ReplyKeyboardMarkup(stop_keyboard, one_time_keyboard=False)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = ''

candy = 0
def start(update, context):
    update.message.reply_text(
        "Привет! Давай играть!",
        reply_markup=markup
    )

def info(update, context):
    update.message.reply_text("Правила игры!\n"
                              "В начале игры нужно ввести общее количество конфет 🍬🍬🍬\n"
                              "Игроки по очереди берут конфеты, но не больше 28 штук 🍭🍭🍭\n"
                              "Побеждает тот, кто последним возьмет конфеты!🏆")

def close(update, context):
    update.message.reply_text("До скорых встреч!👍",
    reply_markup=ReplyKeyboardRemove())

def play(update, context):
    update.message.reply_text("Введите количество 🍬 в игре: ", reply_markup=stop_markup)
    return 1


def play_get_candy(update, context):
    global candy
    candy = int(update.message.text)
    update.message.reply_text("Сколько 🍬 вы возьмете?: ")
    return 2


def player_1(update, context):
    global candy
    try:
        tap = int(update.message.text)
        if 1 <= tap <= 28:
            candy -= int(update.message.text)
            update.message.reply_text(f"🍬 осталось: {candy}.")
        else:
            update.message.reply_text("Возьмите правильное количество!")
            return 2
        if candy > 28:
            #temp = random.randint(1, 28)
            temp = candy % 29
            if candy % 29 == 0:
                temp = 28
            candy -= temp
            update.message.reply_text(f"Бот взял {temp} 🍬.\n"
                                      f"🍬 осталось: {candy}.")
        # elif candy == 0:
        #     update.message.reply_text("Вы победили!😌", reply_markup=markup)
        #     return ConversationHandler.END
        # elif candy > 28:
        #         update.message.reply_text("Сколько 🍬 вы возьмете?")
        #         return 2
            if candy > 28:
                update.message.reply_text("Сколько 🍬 вы возьмете?: ")
            else:
                update.message.reply_text("Вы победили!😌", reply_markup=markup)
                return ConversationHandler.END
            return 2
        else:
            update.message.reply_text("Победил бот!😔", reply_markup=markup)
        return ConversationHandler.END
    except ValueError: update.message.reply_text("Введите число!")
    return 2

def stop(update, context):
    update.message.reply_text("Всего доброго!👍", reply_markup=markup)
    return ConversationHandler.END

play_handler = ConversationHandler(
        entry_points=[CommandHandler('play', play)],
        states={
            1: [MessageHandler(Filters.text & ~Filters.command, play_get_candy)],
            2: [MessageHandler(Filters.text & ~Filters.command, player_1)]

        },
        fallbacks=[CommandHandler('stop', stop)]
    )

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(play_handler)
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("close", close))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
