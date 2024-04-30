import sqlite3


class Order:
    def __init__(self, id_user, name):
        self.id_user = id_user
        self.name = name
        self.product = ''
        self.type = ''
        self.num = 0
        self.cost = 690
        self.state = 'Заказ обрабатывается'

    def __str__(self):
        return f'Пользователь {self.id_user}, {self.product} {self.type} {self.num} шт. – {self.cost} рублей. Состояние: {self.state}'.replace(
            'None ', '')

    async def get_name(self):
        return self.name

    async def get_product(self):
        return self.product

    async def get_type(self):
        return self.type

    async def get_num(self):
        return self.num

    async def get_cost(self):
        return self.cost

    async def get_state(self):
        return self.state

    async def set_product(self, product):
        self.product = product

    async def set_type(self, type):
        self.type = type

    async def set_num(self, num):
        self.num = num

    async def set_cost(self, cost):
        self.cost = cost

    async def set_state(self, state):
        self.state = state


list_of_orders = {}


async def create_order(id_user, name):
    list_of_orders[id_user] = Order(id_user, name)


async def save_order(id_user):
    with sqlite3.connect('orders.db') as con:
        cur = con.cursor()
        product = await list_of_orders[id_user].get_product()
        type_ = await list_of_orders[id_user].get_type()
        num = await list_of_orders[id_user].get_num()
        cost = await list_of_orders[id_user].get_cost()
        state = await list_of_orders[id_user].get_state()
        try:
            cur.execute(
                f"""INSERT INTO orders(id_user, product, type_of_product, num_of_product, cost, state) VALUES({int(id_user)}, "{product}", "{type_}", {num}, {cost}, "{state}")""")
            id = int(cur.execute(f"""SELECT id FROM orders WHERE id_user={id_user}""").fetchall()[-1][0])
        except Exception as e:
            print(e)
    return id


async def get_orders(id_user):
    with sqlite3.connect('orders.db') as con:
        cur = con.cursor()
        orders = cur.execute(f"""SELECT * FROM orders WHERE id_user={id_user}""").fetchall()
        return orders


async def cancel_order(id_order):
    try:
        with sqlite3.connect('orders.db') as con:
            cur = con.cursor()
            cur.execute(f"""DELETE FROM orders WHERE id={id_order}""")
    except Exception as e:
        print(type(e))


async def change_state_order(id_order, state='Заказ принят'):
    try:
        with sqlite3.connect('orders.db') as con:
            cur = con.cursor()
            cur.execute(f"""UPDATE orders SET state = "{state}" WHERE id = {id_order}""")
    except Exception as e:
        print(type(e))

async def get_id_user(id_order: int):
    try:
        with sqlite3.connect('orders.db') as con:
            cur = con.cursor()
            id_user = int(cur.execute(f"""SELECT id_user FROM orders WHERE id={id_order}""").fetchone()[0])
            return id_user
    except Exception as e:
        print(type(e))

async def get_order_from_id(id_order: int):
    try:
        with sqlite3.connect('orders.db') as con:
            cur = con.cursor()
            order = cur.execute(f"""SELECT * FROM orders WHERE id = {id_order}""").fetchone()
        return order
    except Exception as e:
        print(type(e))
