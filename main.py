import telebot
# Импорт модулей из проекта
from config import TOKEN
from extensions import ApiException, Exchange

currencies = {'евро': 'EUR', 'доллар': 'USD', 'рубль': 'RUB'}
# Инициализация объекта робота для телеграмм
bot = telebot.TeleBot(TOKEN)


# Используем декоратор из бота для задания поведения при получении команд
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message,
        'Для использования бота отправьте запрос в данном формате:\n'
        '<имя валюты, цену которой он хочет узнать> <имя валюты, в которой надо узнать цену первой валюты> '
        '<количество первой валюты>'
    )


@bot.message_handler(commands=['values'])
def values(message):
    bot.reply_to(
        message,
        f'Доступные валюты для запроса: {", ".join(currencies.keys())}'
    )


# Используем декоратор из бота для обработки текстовых сообщений
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        # обрабатываем текст входящего сообщения
        base, quote, amount = message.text.split(' ')
        base_ = currencies[base]
        quote_ = currencies[quote]
        amount_ = float(amount)
        # Получаем рассчитанную цену с заданными параметрами
        price = Exchange.get_price(base_, quote_, amount_)
        text = f'Цена {amount} {base_} в {quote_} - {price}'
        bot.send_message(message.chat.id, text)
    # Отлавливаем различные типы исключений
    except ApiException as error:
        bot.send_message(message.chat.id, str(error))
    except KeyError as error:
        bot.send_message(message.chat.id, 'Проверьте правильность ввода валюты')
    except Exception as error:
        print(type(error), error)
        bot.send_message(message.chat.id, 'Ошибка работы программы')


bot.infinity_polling()