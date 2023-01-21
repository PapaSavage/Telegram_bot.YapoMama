import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('new.db')
    cur = db.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS profile(user_id TEXT PRIMARY KEY, name TEXT, number TEXT, adress TEXT)")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS goods(good_id INTEGER PRIMARY KEY, name TEXT, price TEXT, description TEXT, src TEXT, category TEXT)")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS orders(order_id integer PRIMARY KEY, date TEXT, adress TEXT, general_price TEXT, user_id TEXT)")
    db.commit()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS cart(order_id integer, good_id integer, count integer, summa integer, user_id TEXT)")
    db.commit()


async def search_description(name):
    return list(cur.execute(f"SELECT description FROM goods WHERE name == {name}"))

async def search_goods():
    return list(cur.execute("SELECT name, src FROM goods"))
# async def create_order(date):
#     cur.execute("INSERT INTO orders VALUES(NULL, ?, ?, ?, ?)",
#                 ('', '', '', ''))
#     db.commit()
#     return 

# async def edit_order(state, user_id):
#     async with state.proxy() as data:
#         cur.execute(
#             f"UPDATE profile SET good_id = '{data['good_id']}', count = '{data['count']}', summa = '{data['summa']}' WHERE user_id == '{user_id}'")
#         db.commit()

async def create_cart(order_id):
    cur.execute("INSERT INTO orders VALUES(?, ?, ?, ?)",
                (order_id, '', '', '', ''))
    db.commit()
    return

async def edit_cart(state, order_id):
    async with state.proxy() as data:
        cur.execute(
            f"UPDATE profile SET good_oid = '{data['good_id']}' count = '{data['count']}', summa = '{data['summa']}', user_id = '{data['user_id']} WHERE order_id == '{order_id}'")
        db.commit()

async def create_order(date):
    cur.execute("INSERT INTO orders VALUES(NULL, ?, ?, ?, ?)",
                (date, '', '', ''))
    db.commit()
    return 

async def edit_order(state, date):
    async with state.proxy() as data:
        cur.execute(
            f"UPDATE profile SET user_id = '{data['user_id']}', adress = '{data['adress']}', general_price = '{data['general_price']} WHERE date == '{date}'")
        db.commit()

async def create_goods(name, price, description, src, category):
    good = cur.execute("SELECT 1 FROM goods WHERE name == '{key}'".format(
        key=name)).fetchone()
    if not good:
        cur.execute("INSERT INTO goods VALUES(NULL, ?, ?, ?, ?, ?)",
                    (name, price, description, src, category))
        db.commit()

async def create_profile(user_id):
    user = cur.execute("SELECT 1 FROM profile WHERE user_id == '{key}'".format(
        key=user_id)).fetchone()
    if not user:
        cur.execute("INSERT INTO profile VALUES(?, ?, ?, ?)",
                    (user_id, '', '', ''))
        db.commit()


async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            f"UPDATE profile SET name = '{data['name']}', number = '{data['number']}', adress = '{data['adress']}' WHERE user_id == '{user_id}'")
        db.commit()
