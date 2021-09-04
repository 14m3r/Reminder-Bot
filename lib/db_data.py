"""
Database access and tables for mysql
"""

LOGIN = 'login'
PASSWORD = 'password'
DB = 'sale_bot'
HOST = '127.0.0.1'

USERS_TABLE = 'users'

# Example usertable
USERS_TABLE_DATA = "(" \
    "user_id int(11) unsigned NOT NULL DEFAULT 0 UNIQUE, "\
    "perm tinyint NOT NULL DEFAULT 0" \
    ")"

REMINDER_TABLE = 'reminders'


REMINDERS_TABLE_DATA = "(" \
    "rem_id int(11) unsigned NOT NULL DEFAULT 0 UNIQUE," \
    "user_id int(11) unsigned NOT NULL DEFAULT 0," \
    "textstring varchar(256) NOT NULL DEFAULT '', " \
    "date varchar(32) NOT NULL DEFAULT 0 " \
    ")"
