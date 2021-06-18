from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup, CallbackQuery
from utils import dp, parser, User


@dp.message_handler(commands='start')
async def start(message: Message):
    markup = ReplyKeyboardMarkup([[KeyboardButton('Ввести сумму')],
                                  [KeyboardButton('Посчитать курс доллара')],
                                  [KeyboardButton('Бесполезный прикол')]
                                  ],
                                 resize_keyboard=True)
    parser.values[message.from_user.id] = User('')
    await message.answer('Приветствую в нашем боте! Для того, чтобы посчитать вашу прибыль, нажмите на кнопку ниже!\n'
                         'Бот берет курс доллара с <a href="https://api.tinkoff.ru">этого сайта</a>',
                         parse_mode='html',
                         reply_markup=markup)


@dp.message_handler(lambda msg: msg.text == 'Посчитать курс доллара')
async def func(message: Message):
    cur_rate = parser.last_rate
    new_rate = parser.exchange_rate()
    msg = f'Текущий курс {parser.exchange_rate()} руб. за доллар\n'
    if cur_rate != 0:
        msg += f'За время вашего последнего запроса доллар изменился на {(new_rate-cur_rate)/cur_rate*100}%'
    else:
        msg += 'Вы еще не делали запросов на подсчет курса, поэтому бот не может проанализировать изменение.' \
               'Для получения аналитики отправьте запрос еще раз'
    await message.answer(msg)


@dp.message_handler(lambda msg: msg.text == 'Бесполезный прикол')
async def func(message: Message):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text='Купил мужик шляпу', callback_data='call'))
    await message.answer(f'Тык тык тык тык тык', reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data == 'call')
async def data(call: CallbackQuery):
    await call.message.answer_photo('https://pbs.twimg.com/media/D9Xk2DNW4AEXXa8.jpg')
    await call.answer('А она ему как раз', show_alert=True)


@dp.message_handler(lambda msg: msg.text == 'Ввести сумму')
async def func1(message: Message):
    parser.values[message.from_user.id] = User('sum')

    await message.answer('Введите сумму')


@dp.message_handler(lambda msg: msg.from_user.id in parser.values and parser.values[msg.from_user.id].state == 'sum')
async def func2(message: Message):
    if not message.text.isdigit():
        await message.answer('Введите число!')
    else:
        parser.values[message.from_user.id].sum = int(message.text)
        parser.values[message.from_user.id].state = 'sale'
        await message.answer('Введите размер скидки')


@dp.message_handler(lambda msg: msg.from_user.id in parser.values and parser.values[msg.from_user.id].state == 'sale')
async def func3(message: Message):
    if not message.text.isdigit():
        await message.answer('Введите число!')
    else:
        parser.values[message.from_user.id].sale = int(message.text)
        parser.values[message.from_user.id].state = 'per'
        await message.answer('Введите наценку')


@dp.message_handler(lambda msg: msg.from_user.id in parser.values and parser.values[msg.from_user.id].state == 'per')
async def func3(message: Message):
    if not message.text.isdigit():
        await message.answer('Введите число!')
    else:
        await message.answer('Отлично, вот ваш результат!')
        parser.values[message.from_user.id].percent = int(message.text)
        await message.answer(parser.pars(parser.values[message.from_user.id]))
        parser.values[message.from_user.id].reset()




