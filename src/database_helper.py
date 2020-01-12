import mysql.connector as my_sql
import base64

try:
    my_db = my_sql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="shop"
    )
    my_cur = my_db.cursor()
    my_cur.execute(
        """CREATE TABLE IF NOT EXISTS product (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, price DOUBLE NOT NULL, image LONGBLOB NULL, category_name VARCHAR(255) NOT NULL, created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)""")
    my_cur.close()

except ConnectionRefusedError:
    print("Connection Failed")
except Exception as e:
    print(e)


def insert_product(**args):
    new_image = args['image']
    if new_image != None:
        with open(args['image'], 'rb') as fb:
            new_image = fb.read()
    try:
        my_db = my_sql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="shop"
        )
        my_cur = my_db.cursor()
        sql = """INSERT INTO product (name, price, image, category_name) VALUES (%s, %s, %s, %s)"""
        my_cur.execute(
            sql, (args['name'], args['price'],
                  new_image, args['category_name'])
        )
        my_db.commit()
        my_cur.close()
    except ConnectionRefusedError:
        print("Connection Failed")
    except Exception as e:
        raise e


def all_products():
    try:
        my_db = my_sql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="shop"
        )
        my_cur = my_db.cursor()
        my_cur.execute(
            """SELECT id, name, price,category_name, created_at FROM product""")
        all_data = my_cur.fetchall()
        my_cur.close()
        return all_data
    except ConnectionRefusedError:
        print("Connection Failed")
        return []
    except Exception as e:
        print(e)
        return []


def delete_product(product_id):
    try:
        my_db = my_sql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="shop"
        )
        my_cur = my_db.cursor()
        sql = """DELETE FROM product WHERE id = %s"""
        my_cur.execute(sql, (product_id,))
        my_db.commit()
        my_cur.close()
    except ConnectionRefusedError:
        print("Connection Failed")
    except Exception as e:
        print(e)


def update_product(product_id, **args):
    try:
        my_db = my_sql.connect(
            host="localhost",
            user="root",
            passwd="",
            database="shop"
        )
        my_cur = my_db.cursor()
        sql = """UPDATE product SET name = %s, price = %s, category_name = %s WHERE id = %s"""
        my_cur.execute(
            sql, (args['name'], args['price'],
                  args['category_name'], product_id,)
        )
        my_db.commit()
        my_cur.close()
    except ConnectionRefusedError:
        print("Connection Failed")
    except Exception as e:
        raise e
