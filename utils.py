from typing import Tuple
from math import ceil

import requests
from aiogram import Bot, Dispatcher

from config import TOKEN


bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(bot)


class Parser:
    def __init__(self):
        self.values = {}
        self.last_rate = 0

    def pars(self, user) -> str:
        rate = self.exchange_rate()
        spend, pay, profit = 0, 0, 0
        result = 'Потратишь | Заплатит | Получишь\n\n'

        new_line_tuple = self.calculate(user.sum, user.sale, rate, user.percent)
        spend += new_line_tuple[0]
        pay += new_line_tuple[1]
        profit += new_line_tuple[2]

        result += '\n' + self.last_line(spend, pay, profit)
        return result

    @staticmethod
    def last_line(spend: int, pay: int, profit: int) -> str:
        new_line = "Потратишь: {} Руб.\nПолучишь: {} Руб.\nПрибыль: {} Руб.".format(spend, pay, profit)
        return new_line

    @staticmethod
    def calculate(cost: int, sale: int, rate: int, percent: int) -> Tuple[int, int, int , str]:
        cost = ceil((cost*(100-sale)/100)*rate)
        buyer_cost = ceil(cost*(100+percent)/100)
        delta = buyer_cost-cost
        string = f'${cost} Руб.\n\t{buyer_cost} Руб.\n\t{delta} Руб.'
        return cost, buyer_cost, delta, string

    def exchange_rate(self) -> int:
        r = requests.get('https://api.tinkoff.ru/v1/currency_rates?from=USD&to=RUB')
        item = sorted(r.json()['payload']['rates'],
                      key=lambda d: d['category'] == 'DebitCardsTransfers')[0]
        self.last_rate = item['sell']
        return item['sell']


class User:
    def __init__(self, state=''):
        self.state = state
        self.sum = 0
        self.sale = 0
        self.percent = 0

    def reset(self):
        self.state = ''
        self.sum = 0
        self.sale = 0
        self.percent = 0


parser = Parser()