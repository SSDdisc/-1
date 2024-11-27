import telebot
from telebot import types

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)

meeting_types = ["Консультация", "Тренировка", "Встреча", "Вебинар"]

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Добро пожаловать в Бота для бронирования встреч ! Используйте команду /booking для начала.")


@bot.message_handler(commands=['booking'])
def book_meeting(message):
    markup = types.InlineKeyboardMarkup()
    for meeting in meeting_types:
        button = types.InlineKeyboardButton(text=meeting, callback_data=meeting)
        markup.add(button)
    bot.send_message(message.chat.id, "Выберите тип встречи:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    meeting_type = call.data
    bot.answer_callback_query(call.id, f"Вы выбрали: {meeting_type}")

    bot.send_message(call.message.chat.id, "Выберите дату и время для встречи (например,27-11-2024 19:00).")
    bot.register_next_step_handler(call.message, process_date_time, meeting_type)


def process_date_time(message, meeting_type):
    date_time = message.text

    bot.send_message(message.chat.id, f"Вы успешно забронировали встречу типа '{meeting_type}' на {date_time}!")

bot.polling(none_stop=True)