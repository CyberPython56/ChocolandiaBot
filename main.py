from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode, InputMediaPhoto, ReplyKeyboardRemove
from emoji import emojize

from config import TOKEN, names_of_button, id_btn_of_types, alt_name_of_product, id_btn_of_product, types_of_products
from keyboards import inline_menu, set_inline_of_types, keyboard_accept, keyboard_count_of_product
from media import *
from prices import *
from orders import *

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    msg = text(emojize('Привет! Я бот, который сделает твою жизнь слаще!:face_savoring_food:'))
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    await process_menu_command(message)


@dp.message_handler(commands=['menu'])
async def process_menu_command(msg: types.Message):
    await create_order(msg.from_user.id)
    await bot.send_message(msg.from_user.id, bold('Выберите то, что вас интересует:'), reply_markup=inline_menu,
                           parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_back'))
async def process_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await process_menu_command(callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_'))
async def process_buy_type_of_product(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await send_photo_and_price(callback_query)


async def send_photo_and_price(callback_query: types.CallbackQuery):
    data = callback_query.data
    if data.startswith('btn_1'):
        type_ = int(data[-1])
        file = PHOTO_PRODUCT_1[type_]
        price = PRICE_PRODUCT_1[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Трюфели'][type_])
    if data.startswith('btn_2'):
        type_ = int(data[-1])
        file = PHOTO_PRODUCT_2[type_]
        price = PRICE_PRODUCT_2[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Корпусные конфеты'][type_])
    elif data.startswith('btn_7'):
        type_ = int(data[-1])
        file = PHOTO_PRODUCT_7[type_]
        price = PRICE_PRODUCT_7[type_]
        # print(price, type(price))
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Молочные сырки'][type_])
    print(list_of_orders[callback_query.from_user.id])
    file_res = [InputMediaPhoto(file)]
    await bot.send_media_group(callback_query.from_user.id, file_res)
    await bot.send_message(callback_query.from_user.id,
                           text=f'Цена: {price} руб.\nПожалуйста, укажите желаемое количество:',
                           reply_markup=keyboard_count_of_product, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
        product = names_of_button[code]
        await create_order(callback_query.from_user.id)
        await list_of_orders[callback_query.from_user.id].set_product(product)
        print(list_of_orders[callback_query.from_user.id])
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    if id_btn_of_product[code] in id_btn_of_types.keys():
        await bot.send_message(callback_query.from_user.id,
                               bold(f'Выберите вкус {alt_name_of_product[id_btn_of_product[code]]}:'),
                               reply_markup=set_inline_of_types(product=product), parse_mode=ParseMode.MARKDOWN)
    else:
        await send_photo_and_price(callback_query)
    # await process_menu_command(callback_query)


async def accept_buying(msg: types.Message):
    price = await list_of_orders[msg.from_user.id].get_cost()
    cost = price * await list_of_orders[msg.from_user.id].get_num()
    await list_of_orders[msg.from_user.id].set_cost(cost)
    print(list_of_orders[msg.from_user.id])
    await bot.send_message(msg.from_user.id, f'Сумма заказа {cost} рублей. Подтверждаете покупку?',
                           reply_markup=keyboard_accept)


@dp.message_handler(lambda msg: msg.text == 'Да, хочу заказать!')
async def get_accept(msg: types.Message):
    await save_order(id_user=msg.from_user.id)
    await bot.send_message(msg.from_user.id, emojize('Заказ сохранен! Спасибо за покупку!:check_mark_button:'))
    print('[+]Заказ сохранен в БД')
    await process_menu_command(msg=msg)


@dp.message_handler(lambda msg: msg.text.endswith(' шт.') or msg.text == 'В меню')
async def process_buying(msg: types.Message):
    if msg.text.endswith(' шт.'):
        await list_of_orders[msg.from_user.id].set_num(int(msg.text.replace(' шт.', '')))
        await accept_buying(msg)
    elif msg.text == 'В меню':
        await bot.send_message(msg.from_user.id, 'Возвращаюсь в меню...', reply_markup=ReplyKeyboardRemove())
        await process_menu_command(msg)


@dp.message_handler(content_types=['photo'])
async def scan_message(msg: types.Message):
    document_id = msg.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')
    print(f'file_path: {file_info.file_path}')
    print(f'file_size: {file_info.file_size}')
    print(f'file_unique_id: {file_info.file_unique_id}')


@dp.message_handler(content_types=["video"])
async def video_file_id(message: types.Message):
    await bot.send_message(message.from_user.id, "Ваше id video")
    await message.answer(message.video.file_id)


@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(msg: types.Message):
    message_text = text('Я не знаю, что с этим делать :upside-down_face:',
                        italic('\nЯ напоминаю, что есть'),
                        code('команда'), '/help')
    await msg.reply(message_text, parse_mode=ParseMode.MARKDOWN)


if __name__ == '__main__':
    executor.start_polling(dp)
