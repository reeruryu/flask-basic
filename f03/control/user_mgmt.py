from flask_login import UserMixin
from db_model.mysql import conn_mysqldb


class User(UserMixin):
    
    def __init__(self, number, user_id, user_pw):
        self.number = number
        self.user_id = user_id
        self.user_pw = user_pw

    def get_id(self):
        return str(self.number)

    @staticmethod
    def get(number):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE NUMBER = '" + str(number) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(number=user[0], user_id=user[1], user_pw=user[2])
        return user

    @staticmethod
    def find(user_id, user_pw):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + \
            str(user_id) + "' AND USER_PW = '" + \
            str(user_pw) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None

        user = User(number=user[0], user_id=user[1], user_pw=user[2])
        return user
    
    @staticmethod
    def find2(user_id): # 회원가입용 - 중복된 아이디가 있는지
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + \
            str(user_id) + "'"
        # print (sql)
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(number=user[0], user_id=user[1], user_pw=user[2])
        return user

    @staticmethod
    def create(user_id, user_pw): # create 임시로 만든 거
        user = User.find(user_id, user_pw)
        if user == None:
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_ID, USER_PW) VALUES ('%s', '%s')" % (
                str(user_id), str(user_pw))
            db_cursor.execute(sql)
            mysql_db.commit()
            return User.find(user_id)
        else:
            return user
    
    @staticmethod
    def create2(user_id, user_pw): #회원가입용
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "INSERT INTO user_info (USER_ID, USER_PW) VALUES ('%s', '%s')" % (
                str(user_id), str(user_pw))
        db_cursor.execute(sql)
        mysql_db.commit()
        return 1
        
    '''
    # 탈퇴기능
    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)
        mysql_db.commit()
        return deleted
    '''
