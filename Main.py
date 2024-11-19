import time
import telebot
from newspaper import Source
from telebot import types, TeleBot

TOKEN = '6223499719:AAEhZLCvyHG0C6UDxrVVBtMYQVpVsE6LJBg'
CHAT_ID = '770415364'
bot: TeleBot = telebot.TeleBot(TOKEN)


class NewsBot:
    def __init__(self):
        self.i = 0
        self.cnn_paper = Source('https://www.lemonde.fr', language='fr', memoize_articles=False)
        self.cnn_paper.build()

    def find_news(self):
        if self.i >= len(self.cnn_paper.articles):
            return None
        article = self.cnn_paper.articles[self.i]
        article.download()
        article.parse()
        img = article.top_image
        title = article.title
        text = article.text
        self.i += 1
        return img, title, text

    def get_news(self):
        news = []
        article = self.find_news()
        if article:
            news.append(article)
        return news


news_bot = NewsBot()


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Новости")
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)


@bot.message_handler(content_types='text')
def send_news_loop(message):
    if message.text == 'Новости':
        news = news_bot.get_news()
        if news:
            for img, title, text in news:
                if img:
                    bot.send_photo(message.chat.id, photo=img)
                bot.send_message(message.chat.id, text=f'<b>{title}</b>', parse_mode='HTML')

                # Send long text in chunks
                if len(text) > 4096:
                    for x in range(0, len(text), 4096):
                        bot.send_message(message.chat.id, text=f'<i>{text[x:x + 4096]}</i>', parse_mode='HTML')
                else:
                    bot.send_message(message.chat.id, text=f'<i>{text}</i>', parse_mode='HTML')
                time.sleep(1)
        else:
            bot.send_message(message.chat.id, "Не удалось найти новости.")


if __name__ == '__main__':
    bot.send_message(chat_id=CHAT_ID, text='Привет, я присылаю новости из разных источников СМИ.\n'
                                           'Для начала, напиши <b>"/start"</b>.', parse_mode='HTML')
    bot.infinity_polling()
