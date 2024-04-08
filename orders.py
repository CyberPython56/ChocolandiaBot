import sqlite3


class Order:
    def __init__(self, id_user):
        self.id_user = id_user
        self.product = ''
        self.type = ''
        self.num = 0
        self.cost = 690

    def __str__(self):
        return f'Пользователь: {self.id_user}, продукт: {self.product}, вкус: {self.type}, кол-во: {self.num}, стоимость: {self.cost}'

    async def get_product(self):
        return self.product

    async def get_type(self):
        return self.type

    async def get_num(self):
        return self.num

    async def get_cost(self):
        return self.cost

    async def set_product(self, product):
        self.product = product

    async def set_type(self, type):
        self.type = type

    async def set_num(self, num):
        self.num = num

    async def set_cost(self, cost):
        self.cost = cost


list_of_orders = {}


async def create_order(id_user):
    list_of_orders[id_user] = Order(id_user)


async def save_order(id_user):
    with sqlite3.connect('orders.db') as con:
        cur = con.cursor()
        product = await list_of_orders[id_user].get_product()
        type_ = await list_of_orders[id_user].get_type()
        num = await list_of_orders[id_user].get_num()
        cost = await list_of_orders[id_user].get_cost()
        try:
            cur.execute(
                f"""INSERT INTO orders(id_user, product, type_of_product, num_of_product, cost) VALUES({int(id_user)}, "{product}", "{type_}", {num}, {cost})""")
        except Exception as e:
            print(e)


async def get_orders(id_user):
    with sqlite3.connect('orders.db') as con:
        cur = con.cursor()
        orders = cur.execute(f"""SELECT * FROM orders WHERE id_user = {id_user}""").fetchall()
        return orders
