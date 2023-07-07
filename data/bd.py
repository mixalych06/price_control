import psycopg2


class DataBase:
    def __init__(self, dbname, host, user, password):
        self.connection = psycopg2.connect(dbname=dbname, host=host, user=user, password=password)
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS all_product (ID SERIAL PRIMARY KEY NOT NULL,'
                            'seller_id INTEGER, name_seller varchar,'
                            'product_id bigint NOT NULL,'
                            'name_product varchar,'
                            'price INTEGER NOT NULL DEFAULT 0,'
                            'min_price INTEGER NOT NULL DEFAULT 0,'
                            'current_price INTEGER NOT NULL DEFAULT 0,'
                            'flag2 INTEGER NOT NULL DEFAULT 0)')

        self.cursor.execute('CREATE TABLE IF NOT EXISTS admin_user (id_user bigint, '
                            'name1 TEXT, telephone varchar,'
                            'su_admin INTEGER DEFAULT 0,'
                            'user1 INTEGER DEFAULT 0,'
                            'flag1 INTEGER DEFAULT 0, '
                            'flag2 INTEGER DEFAULT 0)')

        self.connection.commit()

    """*********************\/Добавление в базу\/*******************************"""

    def bd_adds_products(self, seller_id, name_seller, product_id, name_product, price):
        """***Добавляет продукт в БД """
        with self.connection.cursor() as cursor:
            cursor.execute("INSERT INTO all_product (seller_id, name_seller, product_id,"
                           "name_product, price, min_price, current_price) "
                           "VALUES (%s, %s, %s, %s, %s, %s, %s)", (seller_id, name_seller, product_id,
                                                               name_product, price, price, price))

    def bd_adds_user(self, id, name, index):
        with self.connection.cursor() as cursor:
            if index in 'admin':
                cursor.execute("INSERT INTO admin_user (id_user, name1, su_admin) "
                               "VALUES (%s, %s, %s)", (id, name, 1))
            elif index in 'user1':
                cursor.execute("INSERT INTO admin_user (id_user, name1, user1) "
                               "VALUES (%s, %s, %s)", (id, name, 1))

    def changes_access(self, user):
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE admin_user SET su_admin = %s,  user1 = %s "
                           "WHERE id_user = %s", user)

    """*********************Частичное изменение зписей в БД *******************************"""

    def bd_changes_the_current_price(self, id_products, price):
        """Изменяет цену товара в БД, если не совпадает с переданной"""
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE all_product SET price = %s WHERE product_id = %s AND price <> %s",
                           (price, id_products, price))

    def bd_changes_min_price(self, id_products, min_price):
        """***Изменяет min цену товара в БД"""
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE all_product SET min_price = %s WHERE product_id = %s",
                           (min_price, id_products))

    def bd_changes_current_price(self, id_products, current_price):
        """***Изменяет min цену товара в БД"""
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE all_product SET current_price = %s WHERE product_id = %s",
                           (current_price, id_products))

    def bd_changes_current_price_all(self):
        """***Уравнивает min цену товара и текущую цену в БД"""
        with self.connection.cursor() as cursor:
            cursor.execute("UPDATE all_product SET min_price = current_price WHERE min_price <> current_price")
            print('or')

    """*********************Выборка данных из БД*******************************"""

    def bd_get_all_sellers(self):
        """Запрос уникальных id магазинов существующих в базе"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT seller_id, name_seller FROM all_product")
            sellers = cursor.fetchall()
            return sellers

    def bd_get_seller_info(self, seller_id):
        """Запрос информации о магазине"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT seller_id, name_seller FROM all_product "
                           "WHERE seller_id = %s", (seller_id,))
            seller = cursor.fetchone()

            return seller

    def bd_get_all_products_seller(self, seller_id):
        """Запрос всех продуктов продавца"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT name_seller, product_id, "
                           "name_product, price, min_price "
                           "FROM all_product WHERE seller_id = %s", (seller_id,))
            sellers = cursor.fetchall()
            return sellers

    def bd_get_amount_tracked_products(self, seller_id):
        '''Отдаёт количество отслеживаемых и не отслеживаемых товара продавца'''
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(min_price)"
                           "FROM all_product WHERE seller_id = %s AND min_price > %s",
                           (seller_id, 0))
            track = cursor.fetchone()
            cursor.execute("SELECT COUNT(min_price)"
                           "FROM all_product WHERE seller_id = %s AND min_price = %s",
                           (seller_id, 0))
            not_track = cursor.fetchone()

            return *track, *not_track

    def bd_get_tracked_products(self, seller_id):
        '''Отдаёт товары'''

        with self.connection.cursor() as cursor:
            cursor.execute("SELECT name_seller, product_id, "
                               "name_product, price, min_price "
                               "FROM all_product WHERE seller_id = %s "
                           "ORDER BY name_product", (int(seller_id),))
            products = cursor.fetchall()
            return products

    def bd_get_products_for_parsing(self):
        """***Отдаёт товары со сниженой ценой"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM all_product WHERE current_price < price - price * 0.15 "
                           "AND min_price <> current_price "
                           "ORDER BY name_seller")
            products = cursor.fetchall()
            return products

    def bd_get_all_users(self):
        """Отдаёт список всех пользователей"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id_user FROM admin_user")
            users = cursor.fetchall()
            return [user[0] for user in users]

    def bd_get_su_admins(self):
        """Отдаёт список всех id суперпользователей"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id_user FROM admin_user WHERE su_admin = %s", (1,))
            users = cursor.fetchall()
            return [user[0] for user in users]

    def bd_get_su_admins_all(self):
        '''Отдаёт список всех суперпользователей'''
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_user WHERE su_admin = %s", (1,))
            users = cursor.fetchall()
            return users

    def bd_get_users(self):
        """Отдаёт список всех id user"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT id_user FROM admin_user WHERE user1 = %s", (1,))
            users = cursor.fetchall()
            return [user[0] for user in users]

    def bd_get_users_all(self):
        """Отдаёт список всех user"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM admin_user WHERE user1 = %s", (1,))
            users = cursor.fetchall()
            return users

    """*********************Удаление данных из БД*******************************"""

    def bd_delete_shop(self, id_seller):
        """Удаляет продукт из БД по id"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM all_product WHERE seller_id = %s", (id_seller,))

    def bd_delete_user(self, id_user):
        """Удаляет продукт из БД по id"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM admin_user WHERE id_user = %s", (id_user,))

    def bd_delete_admin(self, id_user):
        """Удаляет продукт из БД по id"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM admin_user WHERE id_user = %s", (id_user,))
