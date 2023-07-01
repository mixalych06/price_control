import sqlite3


class DataBase:
    def __init__(self, bd_file):
        self.connection = sqlite3.connect(bd_file)
        self.cursor = self.connection
        self.connection.execute('CREATE TABLE IF NOT EXISTS all_product (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                                'seller_id INTEGER, name_seller TEXT,'
                                'product_id INTEGER NOT NULL,'
                                'name_product TEXT,'
                                'price INTEGER NOT NULL DEFAULT 0,'
                                'min_price INTEGER NOT NULL DEFAULT 0,'
                                'flag1 INTEGER NOT NULL DEFAULT 0,'
                                'flag2 INTEGER NOT NULL DEFAULT 0)')

        self.connection.execute('CREATE TABLE IF NOT EXISTS admin_user (id_user INTEGER, '
                                'name TEXT, telephone TEXT,'
                                'su_admin INTEGER DEFAULT 0,'
                                'user INTEGER DEFAULT 0,'
                                'flag1 INTEGER DEFAULT 0, '
                                'flag2 INTEGER DEFAULT 0)')


        self.connection.commit()

    """*********************\/Добавление в базу\/*******************************"""

    def bd_adds_products(self, product_data: list):
        """Добавляет продукт в БД при условии, что его там не"""
        with self.connection:
            x = self.cursor.execute("SELECT * FROM all_product WHERE product_id = ?",
                                    (int(product_data[2]),)).fetchone()
            if not x:
                self.cursor.execute("INSERT INTO all_product (seller_id, name_seller, product_id, name_product, price) "
                                    "VALUES (?, ?, ?, ?, ?)", (product_data))
            self.connection.commit()


    def bd_adds_user(self, id, name, index):
        with self.connection:
            if index in 'admin':
                self.cursor.execute("INSERT INTO admin_user (id_user, name, su_admin) "
                                    "VALUES (?, ?, ?)", (id, name, 1))
            elif index in 'user':
                self.cursor.execute("INSERT INTO admin_user (id_user, name, user) "
                                    "VALUES (?, ?, ?)", (id, name, 1))
            self.connection.commit()


    """*********************Частичное изменение зписей в БД *******************************"""

    def bd_changes_the_current_price(self, id_products, price):
        """Изменяет цену товара в БД, если не совпадает с переданной"""
        try:
            with self.connection:
                self.cursor.execute("UPDATE all_product SET price = ? WHERE product_id = ? AND price <> ?",
                                    (price, id_products, price))
                self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def bd_changes_min_price(self, id_products, min_price):
        """Изменяет min цену товара в БД"""
        with self.connection:
            self.cursor.execute("UPDATE all_product SET min_price = ? WHERE product_id = ?",
                                (min_price, id_products))
            self.connection.commit()

    """*********************Выборка данных из БД*******************************"""

    def bd_get_all_sellers(self):
        """Запрос уникальных id магазинов существующих в базе"""
        with self.connection:
            sellers = self.cursor.execute("SELECT DISTINCT seller_id, name_seller FROM all_product").fetchall()
            return sellers

    def bd_get_seller_info(self, seller_id):
        """Запрос информации о магазине"""
        with self.connection:
            seller = self.cursor.execute("SELECT seller_id, name_seller, COUNT(product_id) FROM all_product "
                                         "WHERE seller_id = ?", (seller_id,)).fetchone()
            return seller

    def bd_get_all_products_seller(self, seller_id):
        """Запрос всех продуктов продавца"""
        with self.connection:
            sellers = self.cursor.execute("SELECT name_seller, product_id, "
                                          "name_product, price, min_price "
                                          "FROM all_product WHERE seller_id = ?", (seller_id,)).fetchall()
            return sellers

    def bd_get_amount_tracked_products(self, seller_id):
        '''Отдаёт количество отслеживаемых и не отслеживаемых товара продавца'''
        with self.connection:
            track = self.cursor.execute("SELECT COUNT(min_price)"
                                        "FROM all_product WHERE seller_id = ? AND min_price > 0",
                                        (seller_id,)).fetchone()
            not_track = self.cursor.execute("SELECT COUNT(min_price)"
                                            "FROM all_product WHERE seller_id = ? AND min_price = 0",
                                            (seller_id,)).fetchone()

            return *track, *not_track

    def bd_get_tracked_products(self, seller_id, tracking_index):
        '''Отдаёт отслеживаемые и не отслеживаемых товары'''
        with self.connection:
            if int(tracking_index) == 1:
                products = self.cursor.execute("SELECT name_seller, product_id, "
                                               "name_product, price, min_price "
                                               "FROM all_product WHERE seller_id = ? AND min_price > 0 "
                                               "ORDER BY name_product", (seller_id,)).fetchall()
            elif int(tracking_index) == 0:
                products = self.cursor.execute("SELECT name_seller, product_id, "
                                               "name_product, price, min_price "
                                               "FROM all_product WHERE seller_id = ? AND min_price = 0 "
                                               "ORDER BY name_product", (seller_id,)).fetchall()

            return products


    def bd_get_products_for_parsing(self):
        '''Отдаёт данные товара для отслеживания'''
        with self.connection:
            products = self.cursor.execute("SELECT * FROM all_product WHERE min_price > 0 AND min_price > price"
                                           " ORDER BY name_seller").fetchall()
        return products

    def bd_get_all_users(self):
        '''Отдаёт список всех пользователей'''
        with self.connection:
            users = self.cursor.execute("SELECT id_user FROM admin_user").fetchall()
        return [user[0] for user in users]

    def bd_get_su_admins(self):
        '''Отдаёт список всех суперпользователей'''
        with self.connection:
            users = self.cursor.execute("SELECT id_user FROM admin_user WHERE su_admin = 1").fetchall()
        return [user[0] for user in users]

    def bd_get_users(self):
        '''Отдаёт список всех user'''
        with self.connection:
            users = self.cursor.execute("SELECT id_user FROM admin_user WHERE user = 1").fetchall()
        return [user[0] for user in users]


    """*********************Удаление данных из БД*******************************"""

    def bd_delete_product(self, id_products):
        """Удаляет продукт из БД по id"""
        with self.connection:
            self.cursor.execute("DELETE FROM seller_id WHERE product_id = ? ", (id_products,))
            self.connection.commit()
