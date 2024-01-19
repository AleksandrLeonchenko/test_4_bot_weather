import telebot
import os
import threading
from telebot import types
from dotenv import load_dotenv

from .models import WeatherData
from .service import get_weather_data

load_dotenv()
stop_flag = threading.Event()
bot = telebot.TeleBot(os.getenv("BOT_TOKEN"))


def get_weather(city: str) -> str:
    """
    Получает информацию о погоде в указанном городе.

    :param city: Название города.
    :return: Сообщение с текущей погодой в городе.
    """
    try:
        weather = get_weather_data(city.lower())
        return f"В городе {city} сейчас температура {weather['temperature']}°C, давление {weather['pressure']} мм.рт.ст, скорость ветра {weather['wind_speed']} м/с."
    except WeatherData.DoesNotExist:
        return f"Извините, информация о погоде в городе {city} не найдена."


@bot.message_handler(commands=["start"])
def start(message):
    """
    Обработчик команды /start. Отправляет сообщение с клавиатурой для узнавания погоды.

    :param message: Объект сообщения от пользователя.
    """
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_weather = types.KeyboardButton("Узнать погоду")
    keyboard.add(button_weather)
    bot.send_message(message.chat.id, 'Введите город', reply_markup=keyboard)


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """
    Обработчик текстовых сообщений. Отправляет сообщение с запросом города для узнавания погоды.

    :param message: Объект сообщения от пользователя.
    """
    if message.text.lower() == "Узнать погоду":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_cancel = types.KeyboardButton("Отмена")
        keyboard.add(button_cancel)
        bot.send_message(message.chat.id, "Введите город:", reply_markup=keyboard)
    else:
        city = message.text
        response = get_weather(city)
        bot.send_message(message.chat.id, response)


def polling():
    """
    Функция, осуществляющая бесконечный опрос бота.

    """
    while not stop_flag.is_set():
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"Error in polling: {e}")


def start_polling():
    """
    Запускает поток для бесконечного опроса бота.

    """
    threading.Thread(target=polling).start()


def stop_polling():
    """
    Останавливает бесконечный опрос бота.

    """
    stop_flag.set()
    bot.stop_polling()
