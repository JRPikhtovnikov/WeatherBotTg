import telebot
import requests
from datetime import datetime, timedelta
from deep_translator import GoogleTranslator
from math import ceil
import json

TOKEN = '6846009581:AAHvR8JUXI1aWZytUClke4SV7h-FcO3YCvo'  # Replace with your actual token
API_KEY = 'c0412242dc37c60853933c6e26613acd'  # Replace with your actual API key
CITY_ID = '498817'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    itembtn1 = telebot.types.KeyboardButton('Сейчас')
    itembtn2 = telebot.types.KeyboardButton('Завтра')
    markup.add(itembtn1, itembtn2)
    bot.send_message(message.chat.id, "Выберите день:", reply_markup=markup)


@bot.message_handler(commands=['week'])
def week(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    for day in days:
        markup.add(telebot.types.KeyboardButton(day))
    bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def handle_keyboard(message):
    if message.text == 'Сейчас':
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&appid={API_KEY}&units=metric')
        if response.status_code == 200:  # Check if the request was successful
            weather_data = response.json()
            bot.send_message(message.chat.id, f'Погода в Санкт-Петербурге сейчас: '
                                              f'{GoogleTranslator(source="auto", target="ru").translate(weather_data["weather"][0]["main"]).lower()}, '
                                              f'температура: {ceil(weather_data["main"]["temp"])}°C')
        else:
            bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Попробуйте позже.")
    elif message.text == 'Завтра':
        tomorrow = datetime.now() + timedelta(days=1)
        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?id={CITY_ID}&appid={API_KEY}&units=metric')
        if response.status_code == 200:  # Check if the request was successful
            forecast = response.json()
            for data in forecast['list']:
                forecast_date = datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d')
                if forecast_date == tomorrow.strftime('%Y-%m-%d'):
                    bot.send_message(message.chat.id, f'Прогноз погоды в Санкт-Петербурге на завтра: '
                                                      f'{GoogleTranslator(source="auto", target="ru").translate(data["weather"][0]["main"]).lower()}, '
                                                      f'температура: {ceil(data["main"]["temp"])}°C')
                    break
        else:
            bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Попробуйте позже.")
    elif message.text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        day_of_week = datetime.now().weekday()
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        chosen_day = days.index(message.text)
        if chosen_day >= day_of_week:
            chosen_day = (chosen_day - day_of_week) + 1
        else:
            chosen_day = (7 - day_of_week + chosen_day) + 1

        response = requests.get(
            f'http://api.openweathermap.org/data/2.5/forecast?id={CITY_ID}&appid={API_KEY}&units=metric')
        if response.status_code == 200:  # Check if the request was successful
            forecast = response.json()
            forecast_date = (datetime.now() + timedelta(days=chosen_day)).strftime('%Y-%m-%d')
            for data in forecast['list']:
                if datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d') == forecast_date:
                    bot.send_message(message.chat.id, f'Прогноз погоды в Санкт-Петербурге на {message.text}: '
                                                      f'{GoogleTranslator(source="auto", target="ru").translate(data["weather"][0]["main"]).lower()},'
                                                      f' температура: {ceil(data["main"]["temp"])}°C')
                    break
        else:
            bot.send_message(message.chat.id, "Не удалось получить данные о погоде. Попробуйте позже.")
    else:
        bot.send_message(message.chat.id, "Неизвестная команда")


# Запуск бота
if __name__ == '__main__':
    bot.polling()
