import telebot

from telebot import types

import secret
import strings
import database

bot = telebot.TeleBot(secret.api_key)


@bot.message_handler(commands=['start'])
def start(message):
    database.init_db()
    markup = types.InlineKeyboardMarkup()
    order_button = types.InlineKeyboardButton(strings.order_button_text, callback_data=strings.order_button_callback)
    review_button = types.InlineKeyboardButton(strings.review_button_text, callback_data=strings.review_button_callback)
    markup.row(order_button, review_button)
    bot.reply_to(message, strings.start_message, reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == strings.order_button_callback:
        handle_order(callback.message)
    if callback.data == strings.review_button_callback:
        handle_review(callback.message)


@bot.message_handler(commands=['review'])
def handle_review(message):
    msg = bot.reply_to(message, strings.review_start_message)
    bot.register_next_step_handler(msg, process_review_step)


def process_review_step(message):
    username = message.from_user.username
    feedback_message = message.text
    database.add_review(username, feedback_message)
    bot.reply_to(message, strings.review_end_message)
    bot.send_message(secret.admin_id, strings.review_admin_message)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, strings.help_text)


@bot.message_handler(commands=['order'])
def handle_order(message):
    msg = bot.reply_to(message, strings.order_start_message)
    bot.register_next_step_handler(msg, process_order_room_step)


def process_order_room_step(message):
    room_number = message.text
    msg = bot.reply_to(message, strings.order_room_step_message)
    bot.register_next_step_handler(msg, process_order_request_step, room_number)


def process_order_request_step(message, room_number):
    username = message.from_user.username
    request_string = message.text
    database.add_order(username, room_number, request_string)
    bot.reply_to(message, strings.order_end_message)
    bot.send_message(secret.admin_id, strings.order_admin_message)


@bot.message_handler()
def invalid_command(message):
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, strings.invalid_command_message)


bot.infinity_polling()
