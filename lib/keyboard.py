from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from .textdata import Buttons
from .db_work import RemindersTable

table = RemindersTable()


class Back:
    btn_back = KeyboardButton(Buttons.back)
    kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_main.add(btn_back)


class Mainmenu:
    btn_add = KeyboardButton(Buttons.addrem)
    btn_del = KeyboardButton(Buttons.delrem)
    btn_list = KeyboardButton(Buttons.remlist)
    btn_adm = KeyboardButton(Buttons.admin)
    kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_main.add(btn_add)
    kb_main.add(btn_del)
    kb_main.add(btn_list)
    kb_main.add(btn_adm)


class Adminmenu:
    btn_mail = KeyboardButton(Buttons.mail)
    kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
    kb_main.add(btn_mail)
    kb_main.add(Back.btn_back)


def deletereminder(user_id):
    rems = range(1, table.count(user_id) + 1)
    kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
    for rem in rems:
        btn_delrem = KeyboardButton(rem)
        kb_main.add(btn_delrem)
    kb_main.add(Back.btn_back)
    return kb_main
