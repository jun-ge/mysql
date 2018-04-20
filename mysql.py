import pymysql


# class Usermsg:
#     def __init__(self, userid, username, useremail, userpassword, userphone):
#         self.userid = userid
#         self.username = username
#         self.userpassword = userpassword
#         self.userphone = userpassword
#         self.useremail = useremail
#
#     def showmsg(self):
#         pass


class DbOperate:
    def __init__(self, path):
        with open(path, "r") as fr:
            for host in fr:
                host = host.strip().split()

        self.db = pymysql.connect(host=host[0], port=int(host[1]), user=host[2],
                                  passwd=host[3], db=host[4], charset='utf8')
        self.cur = self.db.cursor()

    def close(self):
        self.db.close()
        self.cur.close()

    # 单条查询
    def search_one_msg(self):
        self.cur.execute("select * from usermsg")
        date = self.cur.fetchmany(1)
        return date

    # 多条查询
    def search_msg(self, num):
        self.cur.execute("select * from usermsg")
        date = self.cur.fetchmany(num)
        return date

    # 分页查询
    def sybase(self, page, size=10):
        self.cur.execute("select * from usermsg limit %s,%s " % ((page - 1) * size, size))
        date = self.cur.fetchall()
        return date

    # 单条插入
    def insert_one(self, name, email, paswd, phone):
        sql = "INSERT INTO usermsg (USERNAME,EMAIL,PASSWORD,PHONE) values ('{}','{}','{}','{}')".format(name, email,
                                                                                                        paswd, phone)
        print(sql)
        self.cur.execute(sql)
        self.db.commit()

        # self.db.rollback()
        # print("cuowu ")

    # 批量插入
    def insert(self, lst):
        try:
            self.db.begin()
            self.cur.executemany("insert  into usermsg (USERNAME, EMAIL, PASSWORD, PHONE) values(%s, %s, %s, %s)", lst)
            self.db.commit()
        except:
            self.db.rollback()

    # 单条更新
    def update(self, oldname, newname):
        try:
            self.cur.execute("update t_user set username = '{}' where username={}".format(newname, oldname))
            self.db.commit()
        except:
            self.db.rollback()


if __name__ == '__main__':
    path = "./host"
    db = DbOperate(path)
    data = db.search_msg(3)
    print(data)
    db.close()
