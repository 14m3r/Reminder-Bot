from . import db_data
from .masterclass_database import WorkDB


class UserTable(WorkDB):
    def __init__(self):
        self.table = db_data.USERS_TABLE
        self.cols = db_data.USERS_TABLE_DATA
        super().__init__(self.table, self.cols)

    def adduser(self, user_id):
        query = f"INSERT IGNORE INTO {self.table} (user_id) VALUES ({user_id})"
        self._execute_query_without_return(query)

    def mailing(self):
        query =  f"SELECT user_id from {self.table}"
        data = self._execute_query_with_return(query)
        return data



class RemindersTable(WorkDB):
    def __init__(self):
        self.table = db_data.REMINDER_TABLE
        self.cols = db_data.REMINDERS_TABLE_DATA
        super().__init__(self.table, self.cols)

    def getrems(self):
        query = f'select * from {self.table}'
        data = self._execute_query_with_return(query)
        return data

    def delrems(self, rem_id):
        query = f"DELETE FROM {self.table} WHERE rem_id = {rem_id}"
        query1 = f"UPDATE {self.table} SET rem_id=rem_id - 1 WHERE rem_id>={rem_id} "
        self._execute_query_without_return(query, query1)

    def addrem(self, textstring, date, user_id):
        rem_id = self.count(user_id)
        rem_id += 1
        query = f"INSERT INTO {self.table} (rem_id, user_id, textstring, date"\
            f") VALUES ({rem_id}, {user_id}, '{textstring}', '{date}')"
        self._execute_query_without_return(query)

    def count(self, user_id):
        query = f"select count(*) from {self.table} where user_id = {user_id}"
        data = self._execute_query_with_return(query)
        return data[0][0]
