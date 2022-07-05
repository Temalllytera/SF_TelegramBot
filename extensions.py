import datetime
import requests
from config import API


class ApiException(Exception):
    pass


class Exchange:
    data = None
    last_request = None

    @classmethod
    def get_price(cls, base, quote, amount):
        '''возваращаем цену валюты base в валюте quote в количестве amount'''
        # Загружаем данные через API
        cls._get_prices()
        # Выбираем логику в зависимости от указанных валют
        if base == 'USD':
            if quote not in cls.data.keys():
                raise ApiException(f'Валюта {quote} отсутвует в списке')
            price = cls.data[quote]
        elif base in cls.data.keys():
            if quote == 'USD':
                price = 1 / cls.data[base]
            elif quote in cls.data.keys():
                price = cls.data[quote] / cls.data[base]
            else:
                raise ApiException(f'Валюта {quote} отсутвует в списке')
        else:
            raise ApiException(f'Валюта {base} отсутвует в списке')
        return price * amount

    @classmethod
    def _get_prices(cls):
        '''Получаем цены из api

        делаем обращение к api не больше одного раза в час
        '''
        now = datetime.datetime.now()
        if not cls.last_request or cls.last_request + datetime.timedelta(hours=1) < now:
            # Делаем запрос на получение курсов валют к доллару
            r = requests.get(f'https://openexchangerates.org/api/latest.json?app_id={API}')
            # Конвертируем ответ полученный как json в словарь и получаем значение по ключу rates
            cls.data = r.json()['rates']
            # Сохраняем время последнего запроса
            cls.last_request = datetime.datetime.now()
        return cls.data