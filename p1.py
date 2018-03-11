
# class Foo(object):
#
#     def __init__(self,age):
#         self.age = age
#
#     def __add__(self, other):
#         # return self.age + other.age
#         return Foo(self.age + other.age)
#
# obj1 = Foo(19)
# obj2 = Foo(18)
#
# obj3 = obj1 + obj2


import pymysql
dic = {}
CONN = pymysql.connect(**dic)

class MySQLDB(object):

    def __init__(self):
        # 读取配置文件
        dic = {}
        self.conn = pymysql.connect(**dic)

    def fetch(self,sql):
        cursor = self.conn.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        self.conn.close()
        return result


if __name__ == '__main__':

    obj = MySQLDB()
    obj.fetch('select * from tb1')
















