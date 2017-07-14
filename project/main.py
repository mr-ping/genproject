import json
import tornado.ioloop
import tornado.web
import pymysql.cursors
import pymysql
import pymongo
from pymongo import MongoClient


def make_app():
    return tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/mysql", MysqlHandler),
            (r"/mongo", MongoHandler)],
        debug=True)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class MysqlHandler(tornado.web.RequestHandler):
    def get(self):
        res = get_mysql_data()
        self.write(res)


class MongoHandler(tornado.web.RequestHandler):
    def get(self):
        res = get_mongo_data()
        self.write(res)


def get_mongo_data():
    client = MongoClient('mongodb', 27017)
    db = client.MTD
    collection = db.price_collections
    res = collection.find_one()
    if res:
        res['_id'] = str(res['_id'])
    return json.dumps(res, ensure_ascii=False, indent=4)


def get_mysql_data():
    # Connect to the database
    connection = pymysql.connect(
        host='mysql',
        user='root',
        password='111111',
        db='MTD',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT * FROM `rela_product_price` LIMIT 1"
            cursor.execute(sql)
            result = cursor.fetchone()
    finally:
        connection.close()
    return json.dumps(result, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
