from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())
kbI = InlineKeyboardMarkup()
kbR = ReplyKeyboardMarkup()
button = InlineKeyboardButton(text='Расчитать норму калорий', callback_data='calories')
button1 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formula')
kbI.add(button)
kbI.add(button1)

button2 = KeyboardButton(text='Расчитать')
button3 = KeyboardButton(text='Информация')
button4 = KeyboardButton(text='Купить')
kbR.add(button4)
kbR.add(button2)
kbR.add(button3)
kbR.resize_keyboard = True
catalog_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Product1', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product2', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product3', callback_data="product_buying")],
        [InlineKeyboardButton(text='Product4', callback_data="product_buying")],
    ]
)


@dp.message_handler(text=['Купить'])
async def get_buying_list(message):
    with open('files/water.png', 'rb') as img:
        await message.answer_photo(img, 'Название: Product4 | Описание: ноль калорий на весь день | Цена: 100')
    with open('files/protein.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product3 | Описание: Норма калорий в день  | Цена: 200')
    with open('files/burger.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product2 | Описание: Поволяет бстро набрать недостающие калории | '
                                        'Цена: 300')
    with open('files/milk.jpg', 'rb') as img:
        await message.answer_photo(img, 'Название: Product1 | Описание: Поволяет бстро избавится от лишних калори | '
                                        'Цена: 400')
    await message.answer('Выберите продукт для покупки', reply_markup=catalog_kb)

@dp.callback_query_handler(text=['product_buying'])
async def send_confirm_message(call):
    await call.message.answer('Вы выбрали продукт')
    await call.answer()


@dp.message_handler(text=['/start'])
async def start(message):
    await message.answer("Привет", reply_markup=kbR)


@dp.message_handler(text=['Расчитать'])
async def start(message):
    await message.answer("Выбирите опцию", reply_markup=kbI)


@dp.callback_query_handler(text=['formula'])
async def info(call):
    await call.message.answer('Формулы расчёта нормы калорий:\n'
                              '10 * вес(кг) + 6.25 * рост(см) - 5 * возраст(г) + 5 - 161')
    await call.answer()


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Бот расчитывает норму количество калорий для человека')


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text=['calories'])
async def main_menu(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    await message.answer(
        f'Ваша норма калорий: {10 * int(data["weight"]) + 6.25 * int(data["growth"]) - 5 * int(data["age"]) + 5}')
    await state.finish()


@dp.message_handler()
async def all_messages(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
