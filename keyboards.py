from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from config import types_of_products, id_btn_of_types
from emoji import emojize

# Меню
inline_btn_1 = InlineKeyboardButton('Трюфели', callback_data='btn1')
inline_btn_2 = InlineKeyboardButton('Корпусные конфеты', callback_data='btn2')
inline_btn_3 = InlineKeyboardButton('Нарезные конфеты', callback_data='btn3')
inline_btn_4 = InlineKeyboardButton('Шоколадные плитки', callback_data='btn4')
inline_btn_5 = InlineKeyboardButton('Тематические фигурки из шоколада', callback_data='btn5')
inline_btn_6 = InlineKeyboardButton('Шокобомбы', callback_data='btn6')
inline_btn_7 = InlineKeyboardButton('Молочные сырки', callback_data='btn7')
inline_menu = InlineKeyboardMarkup().row(inline_btn_1, inline_btn_4)
inline_menu.row(inline_btn_2, inline_btn_3)
inline_menu.row(inline_btn_6, inline_btn_7)
inline_menu.row(inline_btn_5)

keyboard_accept = ReplyKeyboardMarkup().add(KeyboardButton('Да, хочу заказать!')).add(KeyboardButton('В меню'))
kb_count = [KeyboardButton(f'{x} шт.') for x in range(1, 11)]
keyboard_count_of_product = ReplyKeyboardMarkup()
for i in range(0, 10, 5):
    keyboard_count_of_product.row(*kb_count[i:i + 5])
keyboard_count_of_product.add('В меню')


async def set_keyboard_cancel(orders):
    keyboard_cancel = ReplyKeyboardMarkup()
    kb_orders = [KeyboardButton(f'Отменить заказ №{i}') for i in range(1, len(orders) + 1)]
    for i in range(0, len(orders), 2):
        keyboard_cancel.row(*kb_orders[i:i + 2])
    keyboard_cancel.add('В меню')
    return keyboard_cancel


# Вкусы позиций
async def set_inline_of_types(product: str):
    count_of_btn = id_btn_of_types[product]
    inline_types_of_products = InlineKeyboardMarkup()
    types = sorted(types_of_products[product], key=lambda x: len(x))
    i = 0
    while types:
        if len(types) >= 3:
            if len(types[i]) + len(types[i + 1]) + len(types[i + 2]) <= 35:
                inline_btn_10 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}')
                inline_btn_11 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn + 1}')
                inline_btn_12 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn + 2}')
                count_of_btn += 3
                inline_types_of_products.row(inline_btn_10, inline_btn_11, inline_btn_12)
            elif len(types[i]) + len(types[i + 1]) <= 35:
                inline_btn_10 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}')
                inline_btn_11 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn + 1}')
                count_of_btn += 2
                inline_types_of_products.row(inline_btn_10, inline_btn_11)
            else:
                inline_types_of_products.row(
                    InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}'))
                count_of_btn += 1
        elif len(types) == 2:
            if len(types[i]) + len(types[i + 1]) <= 35:
                inline_btn_10 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}')
                inline_btn_11 = InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn + 1}')
                count_of_btn += 2
                inline_types_of_products.row(inline_btn_10, inline_btn_11)
            else:
                inline_types_of_products.row(
                    InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}'))
                inline_types_of_products.row(
                    InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn + 1}'))
                count_of_btn += 2
        else:
            inline_types_of_products.row(
                InlineKeyboardButton(f'{types.pop(0)}', callback_data=f'btn_{count_of_btn}'))
            count_of_btn += 1
    inline_types_of_products.row(InlineKeyboardButton('Назад', callback_data=f'btn_back'))
    return inline_types_of_products


# Админка
async def confirm_order(id_order):
    confirm = InlineKeyboardMarkup().row(
        InlineKeyboardButton(emojize('Подтвердить заказ:check_mark_button:'), callback_data=f'btn_accept_order{id_order}'),
        InlineKeyboardButton(emojize('Отказать:cross_mark:'), callback_data=f'btn_cancel_order{id_order}'))
    return confirm


menu_admin = InlineKeyboardMarkup()


async def set_admin_menu():
    pass
