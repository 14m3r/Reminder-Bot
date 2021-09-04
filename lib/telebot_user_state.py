"""Addition for PyTelegramApiBOT module user states and saves user input"""


# -*- coding: utf-8 -*-

import sqlite3
import os


DB_PATH = '.t_bot_users_data/user_states_and_data.db'

STATES_TABLE = 'users_state'
DATA_TABLE = 'users_data'


if not os.path.exists('.t_bot_users_data'):
    os.mkdir('.t_bot_users_data')


class SqliteWork():
    def __init__(self, table, rows):
        self.table = table
        self.rows = rows
        self.create_table()

    def create_table(self):
        """Creates default users states table"""
        query = f"CREATE TABLE IF NOT EXISTS {self.table} ({self.rows})"
        self.execute_query(query)

    def execute_query(self, query, with_return=False):
        data = None
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        if with_return:
            data = cursor.fetchall()
        conn.commit()
        conn.close()
        return data


class UserStates():
    """Main user states class"""
    def __init__(self):
        """Inits users states and creates users states file"""
        self.rows = "user_id INT, state TEXT"
        self.table = STATES_TABLE
        self.sqlwork = SqliteWork(self.table, self.rows)

    def add_user(self, user_id):
        """Addition new user in states table"""
        try:
            query = f"SELECT user_id FROM {self.table} WHERE user_id={user_id}"
            self.sqlwork.execute_query(query, True)[0][0]
        except IndexError:
            query = f"INSERT INTO {self.table} (user_id) VALUES({user_id})"
            self.sqlwork.execute_query(query)

    def update_state(self, user_id: int, state: str):
        """Updates user state"""
        query = f"UPDATE {self.table} SET state='{state}' "\
            f"WHERE user_id={user_id}"
        self.sqlwork.execute_query(query)

    def get_current_state(self, user_id: int):
        """Takes from table user state by self.user_id"""
        query = f"SELECT state FROM {self.table} WHERE user_id={user_id}"
        data = self.sqlwork.execute_query(query, True)
        try:
            state = data[0][0]
            return state
        except Exception:
            self.add_user(user_id)
            return 'none'

    def is_current_state(self, user_id: int, *states):
        """Checks users's state and env check_state"""
        cur_state = self.get_current_state(user_id)
        if cur_state in states:
            return True
        return False


class UserData():
    def __init__(self, rows: str):
        # Add to rows user_id
        self.table = DATA_TABLE
        self.rows = 'user_id INT ,' + rows
        self.sqlwork = SqliteWork(self.table, self.rows)

    def create_table(self):
        """Creates default users data table"""
        query = f"CREATE TABLE IF NOT EXISTS {self.table}({self.rows})"
        self.sqlwork.execute_query(query)

    def add_user_in_data(self, user_id: int):
        """Adds user id in data base"""
        query = f"INSERT INTO {self.table} (user_id) VALUES({user_id})"
        self.sqlwork.execute_query(query)

    def get_all_data_by_id(self, user_id: int):
        """Returns all data from base byt user id"""
        query = f"SELECT * FROM {self.table} WHERE user_id={user_id}"
        data = self.sqlwork.execute_query(query, True)
        try:
            return data[0]
        except IndexError:
            return ("empty",)

    def add_data(self, user_id: int, key, data):
        """Adds data for user_id with key"""
        query = f"UPDATE {self.table} SET {key}='{data}' "\
            f"WHERE user_id={user_id}"
        self.sqlwork.execute_query(query)

    def drop_data(self, user_id: int):
        """Remove all saved user data from base"""
        query = f"DELETE FROM {DATA_TABLE} WHERE user_id={user_id}"
        self.sqlwork.execute_query(query)

