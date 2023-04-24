import requests
from config import api_weather,api_rate
from transliterate import translit

url_weather = 'https://api.openweathermap.org/data/2.5/weather'
url_rate = 'https://api.apilayer.com/exchangerates_data/convert'


def get_weather_info(city):
    '''
    функция get_weather_info принимает название города в виде строки,
    возвращает словарь содержащий характеристики погоды в городе
    '''
    #Формирование параметров для get запроса
    params_weather = {
        'q': translit(city, language_code='ru', reversed=True),
        'appid': api_weather
    }
    response = requests.get(url_weather, params=params_weather)
    if response.status_code == 404:
        return False
    response_js = response.json()
    #Формирование выходных данных функции с характеристиками погоды
    data={
        'city': city.capitalize(),
        'temp': int(response_js['main']['temp']-273),
        'wind': response_js['wind']['speed']

    }
    return data


def get_rate_info(to, from_, amount):
    '''
    функция get_rate_info принимает пару для конвертации и сумму, возращает словарь
    содержащий данные о  конвертации
    '''
    params_rate = {
        'to': to,
        'from': from_,
        'amount': amount
    }
    response = requests.get(url_rate,params=params_rate, headers={'apikey': api_rate})
    if response.status_code > 500: #Ошибка сервера
        return {'status': 'connect_error'}

    if response.status_code == 400: #Ошибки связаные с передаными данными
        if '"to"' in response.json()['error']['message']:
            return {'status': 'to_error'}
        elif '"from"' in response.json()['error']['message']:
            return {'status': 'from_error'}
        elif 'amount' in response.json()['error']['message']:
            return {'status': 'amount_error'}
    data = {
        'status': 'success',
        'to': to,
        'from': from_,
        'amount': amount,
        'result': response.json()['result']
    }
    return data



