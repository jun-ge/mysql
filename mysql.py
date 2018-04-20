import pymysql


class Usermsg:
    def __init__(self, userid, username, useremail, userpassword, userphone):
        self.userid = userid
        self.username = username
        self.userpassword = userpassword
        self.userphone = userpassword
        self.useremail = useremail

    def showmsg(self):
        pass


class DbOperate:
    def __init__(self, host, port, user, passwd, dbs, charset):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.dbs = dbs
        self.charset = charset
        self.getconn()

    def getconn(self):
        self.db = pymysql.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.dbs,
                                  charset=self.charset)
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
        try:
            sql = "INSERT INTO usermsg (USERNAME, EMAIL, PASSWORD, PHONE) values ('{}',{},{},{})".format(name, email, paswd, phone)
            self.cur.execute(sql)
            self.db.commit()
        except:
            self.db.rollback()

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

    hosts = []
    with open("host", "r") as fr:
        for host in fr:
            host = host.split()
            hosts.append(host)

    HOST = hosts[1][0]
    PORT = hosts[1][1]
    USER = hosts[1][2]
    PASSWD = hosts[1][3]
    DATEBASE = hosts[1][4]
    CHARSET = 'utf8'

    db = DbOperate(HOST, PORT, USER, PASSWD, DATEBASE, CHARSET)

    db.insert_one('烟烟烟', 'y', 'y', 'y')
    msg = db.sybase(1, 10)
    print(msg)
    db.close()
