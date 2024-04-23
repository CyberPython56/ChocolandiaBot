from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code
from aiogram.types import ParseMode, InputMediaPhoto, ReplyKeyboardRemove
from emoji import emojize
from datetime import datetime

from config import TOKEN, id_btn_of_types, alt_name_of_product, id_btn_of_product, types_of_products
from keyboards import inline_menu, set_inline_of_types, keyboard_accept, keyboard_count_of_product, set_keyboard_cancel, \
    confirm_order
from media import *
from prices import *
from orders import *
from admin import ADMINS_ID

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    msg = text(emojize('Привет! Я бот, который сделает твою жизнь слаще!:face_savoring_food:'))
    await bot.send_message(message.from_user.id, msg, parse_mode=ParseMode.MARKDOWN)
    await process_menu_command(message)


@dp.message_handler(commands=['help'])
async def help(msg: types.Message):
    await bot.send_message(msg.from_user.id, emojize('Я бот, который поможет тебе наполнить свою жизнь '
                                                     'шоколадом:chocolate_bar:\nВот мои команды:\n/start\n/menu\n/orders'
                                                     '\n/cancel_order\nЕсли хочешь себе такого же бота, то напиши '
                                                     'моему создателю @CyberPyth0n'))


@dp.message_handler(commands=['menu'])
async def process_menu_command(msg: types.Message):
    await create_order(msg.from_user.id, msg.from_user.first_name)
    await bot.send_message(msg.from_user.id, bold('Выберите то, что вас интересует:'), reply_markup=inline_menu,
                           parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_back'))
async def process_back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await process_menu_command(callback_query)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_accept_order'))
@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_cancel_order'))
async def process_state_order(callback_query: types.CallbackQuery):
    if callback_query.data.startswith('btn_accept_order'):
        id_order = int(callback_query.data[callback_query.data.index('order') + 5:])
        await change_state_order(id_order)
        await bot.send_message(callback_query.from_user.id, bold(f'Заказ №{id_order} принят'),
                               reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)
    elif callback_query.data.startswith('btn_cancel_order'):
        id_order = int(callback_query.data[callback_query.data.index('order') + 5:])
        # await change_state_order(id_order)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn_'))
async def process_buy_type_of_product(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await send_photo_and_price(callback_query)


async def send_photo_and_price(callback_query: types.CallbackQuery):
    data = callback_query.data
    flag = False
    if data.startswith('btn_1'):
        type_ = int(data[-1])
        file = [PHOTO_PRODUCT_1[type_]]
        price = PRICE_PRODUCT_1[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Трюфели'][type_])
    elif data.startswith('btn_2'):
        type_ = int(data[-1])
        file = [PHOTO_PRODUCT_2[type_]]
        price = PRICE_PRODUCT_2[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Корпусные конфеты'][type_])
    elif data.startswith('btn3'):
        file = [PHOTO_PRODUCT_3[x] for x in PHOTO_PRODUCT_3.keys()]
        price = PRICE_PRODUCT_3[0]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
    elif data.startswith('btn_4'):
        type_ = int(data[-1])
        file = [PHOTO_PRODUCT_4[x] for x in PHOTO_PRODUCT_4]
        price = PRICE_PRODUCT_4[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Шоколадные плитки'][type_])
    elif data.startswith('btn5'):
        file = [PHOTO_PRODUCT_5[x] for x in PHOTO_PRODUCT_5.keys()]
        price = PRICE_PRODUCT_5[0]
        flag = True
        await list_of_orders[callback_query.from_user.id].set_cost(price)
    elif data.startswith('btn6'):
        file = [PHOTO_PRODUCT_6[x] for x in PHOTO_PRODUCT_6.keys()]
        price = PRICE_PRODUCT_6[0]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
    elif data.startswith('btn_7'):
        type_ = int(data[-1])
        file = [PHOTO_PRODUCT_7[type_]]
        price = PRICE_PRODUCT_7[type_]
        await list_of_orders[callback_query.from_user.id].set_cost(price)
        await list_of_orders[callback_query.from_user.id].set_type(types_of_products['Молочные сырки'][type_])
    file_res = [InputMediaPhoto(x) for x in file]
    await bot.send_media_group(callback_query.from_user.id, file_res)
    if flag:
        await bot.send_message(callback_query.from_user.id,
                               f'По поводу фигурок жду ваших сообщений в личном чате, для договора о тематике @kkatia0.'
                               f' Стоимость одной фигурки {PRICE_PRODUCT_5[0]} рублей')
        await process_menu_command(callback_query)
    else:
        name = bold(id_btn_of_product[int(str([x for x in data if x.isdigit()][0]))])
        await bot.send_message(callback_query.from_user.id,
                               text=f'{name}\nЦена: {price} руб.\nПожалуйста, укажите желаемое количество:',
                               reply_markup=keyboard_count_of_product, parse_mode=ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    if code.isdigit():
        code = int(code)
        product = id_btn_of_product[code]
        await create_order(callback_query.from_user.id, callback_query.from_user.first_name)
        await list_of_orders[callback_query.from_user.id].set_product(product)
        await print_info(callback_query)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    if id_btn_of_product[code] in id_btn_of_types.keys():
        await bot.send_message(callback_query.from_user.id,
                               bold(f'Выберите вкус {alt_name_of_product[id_btn_of_product[code]]}:'),
                               reply_markup=await set_inline_of_types(product=product), parse_mode=ParseMode.MARKDOWN)
    else:
        await list_of_orders[callback_query.from_user.id].set_type(None)
        await send_photo_and_price(callback_query)


async def accept_buying(msg: types.Message):
    price = await list_of_orders[msg.from_user.id].get_cost()
    cost = price * await list_of_orders[msg.from_user.id].get_num()
    await list_of_orders[msg.from_user.id].set_cost(cost)
    await print_info(msg)
    await bot.send_message(msg.from_user.id, f'Сумма заказа {cost} рублей. Подтверждаете покупку?',
                           reply_markup=keyboard_accept)


@dp.message_handler(lambda msg: msg.text == 'Да, хочу заказать!')
async def get_accept(msg: types.Message):
    id_order = await save_order(id_user=msg.from_user.id)
    await bot.send_message(msg.from_user.id, emojize(
        'Заказ сохранен! Спасибо за покупку!:check_mark_button:\nДля просмотра заказов используйте команду /orders'),
                           reply_markup=ReplyKeyboardRemove())
    print(f'[+]Заказ №{id_order} сохранен в БД –––', msg.from_user.first_name, str(datetime.now())[:18])
    for admin in [admin for admin in ADMINS_ID.keys() if ADMINS_ID[admin]]:
        await bot.send_message(admin, emojize(
            ':check_mark_button:' + bold(f'Новый заказ №{id_order}: ')) + f'{list_of_orders[msg.from_user.id]}',
                               parse_mode=ParseMode.MARKDOWN, reply_markup=await confirm_order(id_order))
    await process_menu_command(msg=msg)


@dp.message_handler(lambda msg: msg.text.endswith(' шт.') or msg.text == 'В меню')
async def process_buying(msg: types.Message):
    if msg.text.endswith(' шт.'):
        await list_of_orders[msg.from_user.id].set_num(int(msg.text.replace(' шт.', '')))
        await accept_buying(msg)
    elif msg.text == 'В меню':
        await bot.send_message(msg.from_user.id, 'Возвращаюсь в меню...', reply_markup=ReplyKeyboardRemove())
        await process_menu_command(msg)


@dp.message_handler(commands=['orders'])
async def send_orders(msg: types.Message):
    orders = await get_orders(msg.from_user.id)
    orders_string = [
        bold(order[2]) + ' ' + order[3] + ' ' + str(order[4]) + ' шт.\n' + italic('Итоговая стоимость: ') + str(
            order[5]) + ' рублей.' + italic('\nСостояние: ') + order[6].lower() for order in orders]
    if len(orders_string) < 10:
        orders_string = '\n'.join([f':keycap_{i + 1}:' + orders_string[i] for i in range(len(orders_string))]).replace(
            'None ', '')
    elif len(orders_string) < 20:
        orders_string_10 = '\n'.join([f':keycap_{i + 1}:' + orders_string[i] for i in range(10)]).replace(
            'None ', '')
        orders_string_20 = '\n'.join(
            [':keycap_1:' + f':keycap_{(i % 10) + 1}:' + orders_string[i] for i in
             range(10, len(orders_string))]).replace(
            'None', '')
        orders_string = orders_string_10 + '\n' + orders_string_20
    await bot.send_message(msg.from_user.id, emojize(f'Ваши заказы:\n{orders_string}'), parse_mode=ParseMode.MARKDOWN)
    await bot.send_message(msg.from_user.id,
                           'Для отмены заказа используйте  команду /cancel_order\nДля возврата в меню /menu')


@dp.message_handler(lambda msg: msg.text.startswith('Отменить заказ №'))
async def process_cancel_order(msg: types.Message):
    num_order = int(msg.text[-1])
    orders = await get_orders(msg.from_user.id)
    await cancel_order(orders[num_order - 1][0])
    await bot.send_message(msg.from_user.id,
                           f'Заказ №{num_order} ' + italic(f'{orders[num_order - 1][2]}') + ' отменен.',
                           reply_markup=ReplyKeyboardRemove(), parse_mode=ParseMode.MARKDOWN)
    print(f'[-]Заказ №{orders[num_order - 1][0]} удален –––', msg.from_user.first_name, str(datetime.now())[:18])
    for admin in [admin for admin in ADMINS_ID.keys() if ADMINS_ID[admin]]:
        await bot.send_message(admin, emojize(':cross_mark:' + bold(f'Отмена заказа №: {orders[num_order - 1][0]}')),
                               parse_mode=ParseMode.MARKDOWN)
    await process_menu_command(msg)


@dp.message_handler(commands=['admin'])
async def admin(msg: types.Message):
    if msg.from_user.id in ADMINS_ID.keys():
        ADMINS_ID[msg.from_user.id] = True
        await bot.send_message(msg.from_user.id, emojize('Вы вошли в режим админа:unlocked:'))
    else:
        await bot.send_message(msg.from_user.id, emojize('К сожалению, вы не являетесь админом:worried_face:'))


@dp.message_handler(commands=['admin_off'])
async def admin(msg: types.Message):
    if msg.from_user.id in ADMINS_ID.keys():
        ADMINS_ID[msg.from_user.id] = False
        await bot.send_message(msg.from_user.id, emojize('Вы вышли из режима админа:locked:'))
    else:
        await bot.send_message(msg.from_user.id, emojize('К сожалению, вы не являетесь админом:worried_face:'))
    await process_menu_command(msg)


@dp.message_handler(commands=['cancel_order'])
async def get_num_cancel_order(msg: types.Message):
    orders = await get_orders(msg.from_user.id)
    await bot.send_message(msg.from_user.id, 'Пришлите номер заказа, который хотите отменить',
                           reply_markup=await set_keyboard_cancel(orders))


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
    message_text = text('Я не знаю, что с этим делать:pensive_face:\nЯ напоминаю, что есть',
                        code('команда'), '/help')
    await msg.reply(emojize(message_text), parse_mode=ParseMode.MARKDOWN)
    await process_menu_command(msg)


async def print_info(msg):
    print(msg.from_user.first_name, msg.from_user.username, '–', list_of_orders[msg.from_user.id],
          '' + str(datetime.now().time())[:8])


if __name__ == '__main__':
    try:
        executor.start_polling(dp)
    except Exception as e:
        print(e)
