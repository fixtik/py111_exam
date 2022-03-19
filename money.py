import sys
from typing import Any
import requests
import json
import os
import datetime


# Реализовать класс Money.
# Продумать как хранить значение и обосновать свой выбор
#
# Пример:
# Money(whole:int, remains: int)  # целые отдельно, остаток отдельно (рубли и копейки)
# Money(value:int)  # значение в минимальной денежной единице (копейки, центы)
# Money(value:float)  # значение с плавающей запятой
# Также добавить атрибут с названием валюты классу наследнику.
#
# Реализовать:
# 1. Сложение экземпляров класса  # Money(9, 10) + Money(1, 20) = Money(10, 30). просто пример для Money(whole:int, remains: int)
# 2. Вычитание экземпляров.
# 3. Умножение/деление экземпляра на число.
# 4. Реализовать операции сравнения. (==, !=, <, >, <=, >=) # Money(100) > Money(90) -> True
# 							  # Money(100) > Money(200) -> False
# 5. Реализовать метод класса convert_to_usd() -> Money(value in usd)
# 6. Реализовать метод класса convert_to_valute(valute:str) -> Money(value in valute)
#    Валюта должна конвертироваться по текущему курсу ЦБ.
# 7. Кэширование последних кусров при запуске скрипта, если интернет отключен, брать значение для конвертации из кэша. (json, sqlite, pickle и т.д.)
# 8. *Хранить дату последнего обновления кэша
#
# Требования:
# 1. Докстринги;
# 2. Типизация;
# 3. Проверка типов;
# 4. Соответствие pep8;
# 5. Небольшой сценарий использования базового класса;
# 6. Создать дочерний класс, конкретной валюты;
# 7*. Тестирование.
#
# ХАЛП:
# 1. При реализации вспомнить переопределение "магических" методов для сравнения объектов.
# 2. Получение курса с ЦБ гуглится за 10-15 минут. Используем библиотеку requests.

class Money:
    CURRENCY = {'RUR', 'USD', 'EUR'}

    def __init__(self, value: float, currency: str = 'RUR'):
        self.value = self._check_items(value)
        self.currency = self._available_currency(currency)
        self._actual_date = None
        self._availeble_currency = None


    @staticmethod
    def _check_items(check_value: Any) -> float:
        """проверка вводимых данных"""
        if not isinstance(check_value, (int, float)):
            raise TypeError(f'Ожидается (int, float), получено {type(check_value)}')
        return float(check_value)

    def _available_currency(self, entring_cur: str) -> str:
        if not (entring_cur in self.CURRENCY):
            raise ValueError(f'C валютой {entring_cur} еще не работаем')
        return entring_cur

    def __available_to_compare(self, other: Any) -> bool:
        """проверка возможности производства действий с двумя объектами"""
        return isinstance(other, Money) and (self.currency == other.currency)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value},{self.currency})'

    def __str__(self):
        return f'значение: {self.value}, валюта: {self.currency}'

    def __eq__(self, other: 'Money') -> bool:
        """определяет поведение оператора =="""
        if self.__available_to_compare(other):
            return self.value == other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __ne__(self, other: 'Money') -> bool:
        if self.__available_to_compare(other):
            return self.value != other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __lt__(self, other: 'Money') -> bool:
        """определяет поведение оператора меньше, <"""
        if self.__available_to_compare(other):
            return self.value < other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __gt__(self, other: 'Money') -> bool:
        """Определяет поведение оператора больше, >"""
        if self.__available_to_compare(other):
            return self.value > other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __le__(self, other: 'Money') -> bool:
        """Определяет поведение оператора меньше или равно, <="""
        if self.__available_to_compare(other):
            return self.value <= other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __ge__(self, other: 'Money') -> bool:
        """Определяет поведение оператора больше или равно, >="""
        if self.__available_to_compare(other):
            return self.value >= other.value
        else:
            raise TypeError("Невозможно сравнить")

    def __add__(self, other: 'Money') -> float:
        """
        Сложение
        если второе слогаемое непонятного типа - ничего не изменяется
        """
        if self.__available_to_compare(other):
            self.value += other.value
            return self.value

    def __sub__(self, other: 'Money') -> float:
        """"Вычитание. По аналогии со сложением"""
        if self.__available_to_compare(other):
            self.value -= other.value
            return self.value

    def __mul__(self, other: (int, float)) -> float:
        """
        Умножение на число
        :param other: int, float
        :return: self.value
        """
        self._check_items(other)
        self.value *= other
        return self.value

    def __floordiv__(self, other: (int, float)) -> int:
        """
        Умножение на число
        :param other: int, float
        :return: результат целочисленного деления
        """
        self._check_items(other)
        return self.value // other

    def __truediv__(self, other: (int, float)) -> float:
        """Деление, оператор /."""
        self._check_items(other)
        self.value /= other
        return self.value

    def get_current_exchange_rate(self) -> {}:
        """
        получение курса валют с сайта ЦБ
        :return словарь с данными с сайта ЦБ
        """
        # попытка получения свежих данных
        try:
            requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
            responce = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
            with open('cache.json', 'w+') as f:
                json.dump(responce, f)
        # упс, Интернет-соединения нет, достаем из файла
        except requests.ConnectionError:
            print("Нет Интернет-соединения с сайтом ЦБ")
            responce = self._read_cache_file()
        return responce

    def _read_cache_file(self) -> {}:
        """
        чтение кэш-файла, если он есть
        :return: словарь с последними полученными данными из ЦБ
        """
        if not (os.path.isfile('cache.json')):
            raise Exception("Не могу получить данные из кэша!")
        with open('cache.json', 'r') as f:
            return json.load(f)

    def _inner_exchange_currency(self, value: (int, float) = 1, from_currency: str = 'RUR', to_currency: str = 'USD') -> float:
        """
        Внутренняя функция конвертации
        :param value: количество конвертируемой валюты
        :param from_currency: исходная валюта
        :param to_currency: конечная валюта
        :return: полученное значение
        """
        if not self._availeble_currency:
            raise ValueError("Без актуальных курсов валют не могу произвести конвертацию!")
        if from_currency == "RUR":
            return value / self._availeble_currency[to_currency]['Value']
        if to_currency == "RUR":
            return value * self._availeble_currency[from_currency]['Value']

    def _update_inner_info(self) -> None:
        """
        Обновление данных
        """
        info = self.get_current_exchange_rate()
        actual_date = datetime.datetime.fromisoformat(info['Date'])
        self._actual_date = actual_date.strftime("%d.%m.%Y %H:%M:%S")
        self._availeble_currency = info['Valute']

    def _double_exchange(self, value: (int,float) = 1, from_currency: str = 'RUR', to_currency: str = 'USD') -> float:
        """
        Двойная конвертация через RUR
        :param value: количество конвертируемой валюты
        :param from_currency: код исходной валюты
        :param to_currency: код валюты для конвертации
        :return: результат конвертации
        """
        temp_value = self._inner_exchange_currency(value, from_currency, 'RUR')
        return self._inner_exchange_currency(temp_value, "RUR", to_currency)

    def exchange_currency(self, value: (int,float) = 1, from_currency: str = 'RUR', to_currency: str = 'USD') -> str:
        """
        функция конвертации валют
        :param value: количество конвертируемой валюты
        :param from_currency: код исходной валюты
        :param to_currency: код валюты для конвертации
        :return: строка с результатом и пояснениями
        """
        self._update_inner_info()
        if (to_currency in self._availeble_currency) or to_currency == 'RUR':
            # если нужна двойная конвертация
            if from_currency != "RUR" and to_currency != "RUR":
                temp_value = self._double_exchange(value, from_currency, to_currency)
            else:
                temp_value = self._inner_exchange_currency(value, from_currency, to_currency)
            return f'На {self._actual_date} конвертация {value} {from_currency} = {temp_value} {to_currency}'
        else:
            print(f'На {self._actual_date} ЦБ РФ не располагает сведениями о валюте "{to_currency}"')

    def convert_to_valute(self, to_currency: str = 'USD') -> 'Money':
        """
        Конвертация внутри объекта Money
        :param to_currency: в какую валюту конвертируем
        :return: объект Money
        """
        self._update_inner_info()
        if self.currency != "RUR" and to_currency != "RUR":
            self.value = self._double_exchange(self.value, self.currency, to_currency)
        else:
            self.value = self._inner_exchange_currency(self.value, self.currency, to_currency)
        self.currency = to_currency
        return self

    def show_last_update_date(self) -> None:
        """Выводит время последнего обновления данных (кэша)"""
        if not (self._actual_date is None):
            print(self._actual_date)
        else:
            actual_date = datetime.datetime.fromisoformat(self._read_cache_file()['Date'])
            self._actual_date = actual_date.strftime("%d.%m.%Y %H:%M:%S")
            print(self._actual_date)

    def show_actual_ecxenge_rate(self):
        self._update_inner_info()
        for key, item in self._availeble_currency.items():
            print(f'{item["Name"]:<50} Код валюты {item["CharCode"]:<20} текущий курс  {item["Value"]} Руб')




if __name__ == '__main__':
    rur = Money(5)
    rur2 = Money(10)
    usd = Money(100, 'USD')
    eur = Money(100, "EUR")

    rur.show_last_update_date()
    rur.show_actual_ecxenge_rate()

   # print(rur2 > usd.convert_to_valute("RUR"))
    print(rur2 == rur)
    print(usd > eur.convert_to_valute("USD"))


