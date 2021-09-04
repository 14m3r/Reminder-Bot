import telebot
import config
import lib.keyboard as kb
import lib.textdata as textdata
import lib.telebot_user_state
import lib.db_work
import time_monitoring
import lib.input_check
import threading

data_row = "remind TEXT"

table_users = lib.db_work.UserTable()
table_remind = lib.db_work.RemindersTable()
user_data = lib.telebot_user_state.UserData(data_row)

bot = telebot.TeleBot(config.TOKEN)

telebot.apihelper.proxy = {'https': 'socks5://127.0.0.1:9050'}

user_states = lib.telebot_user_state.UserStates()


def backToMainmenu(msg):
    bot.send_message(
        msg.chat.id,
        textdata.Messages.mainmenu,
        reply_markup=kb.Mainmenu.kb_main
    )
    user_states.update_state(msg.chat.id, textdata.States.mainmenu)


@bot.message_handler(commands=['start'])
def start(msg):
    table_users.adduser(msg.chat.id)
    user_states.add_user(msg.chat.id)
    user_data.add_user_in_data(msg.chat.id)
    backToMainmenu(msg)


# MAIN MENU
@bot.message_handler(
    func=lambda msg: user_states.is_current_state(
        msg.chat.id, textdata.States.mainmenu
        )
    )
def mainmenu(msg):
    if msg.text == textdata.Buttons.addrem:
        bot.send_message(
            msg.chat.id,
            textdata.Messages.addrem_m,
            reply_markup=kb.Back.kb_main
        )
        user_states.update_state(msg.chat.id, textdata.States.addrem_m)

    if msg.text == textdata.Buttons.delrem:
        bot.send_message(
            msg.chat.id,
            textdata.Messages.delrem,
            reply_markup=kb.deletereminder(msg.chat.id)
        )
        user_states.update_state(msg.chat.id, textdata.States.delrem)

    if msg.text == textdata.Buttons.remlist:
        data = table_remind.getrems()
        for i in data:
            message = f"Номер:{i[0]}, Текст:{i[2]}, Дата:{i[3]}"
            bot.send_message(msg.chat.id, message)
        if data == ' ':
            bot.send_message(msg.chat.id, 'Оповещений нет.')
    if msg.text == textdata.Buttons.admin:
        bot.send_message(
            msg.chat.id,
            textdata.Messages.admin,
            reply_markup=kb.Adminmenu.kb_main
        )
        user_states.update_state(
            msg.chat.id, textdata.States.admin
        )


# ADD REMINDER
@bot.message_handler(
    func=lambda msg: user_states.is_current_state(
        msg.chat.id, textdata.States.addrem_m
    )
)
def add_reminder(msg):
    if msg.text == textdata.Buttons.back:
        backToMainmenu(msg)
        return
    user_data.add_data(msg.chat.id, 'remind', msg.text)
    user_states.update_state(msg.chat.id, textdata.States.addrem_d)
    bot.send_message(msg.chat.id, textdata.Messages.addrem_d)


@bot.message_handler(
    func=lambda msg: user_states.is_current_state(
        msg.chat.id, textdata.States.addrem_d
    )
)
def add_reminder_date(msg):
    if msg.text == textdata.Buttons.back:
        backToMainmenu(msg)
        return

    check, option = lib.input_check.time(msg.text)
    if check:
        data = time_monitoring.getdatetime(msg.text, option)
        texstring = user_data.get_all_data_by_id(msg.chat.id)
        table_remind.addrem(texstring[1], data, msg.chat.id)
        bot.send_message(msg.chat.id, 'Ваше оповещение добавлено')
        backToMainmenu(msg)
    else:
        bot.send_message(msg.chat.id, 'Неправильно введено время')


# DELETE REMINDER
@bot.message_handler(
    func=lambda msg: user_states.is_current_state(
        msg.chat.id, textdata.States.delrem
    )
)
def delete_menu(msg):
    if msg.text == textdata.Buttons.back:
        backToMainmenu(msg)
        return

    table_remind.delrems(msg.text)
    bot.send_message(msg.chat.id, 'Оповещение удалено')
    backToMainmenu(msg)

# ADMIN MENU
@bot.message_handler(
    func=lambda msg: user_states.is_current_state(
        msg.chat.id, textdata.States.admin
    )
)
def admin_menu(msg):
    if msg.text == textdata.Buttons.back:
        backToMainmenu(msg)
        return

    if msg.text == textdata.Buttons.mail:
        bot.send_message(msg.chat.id,
                         textdata.Messages.mail,
                         reply_markup=kb.Back.kb_main
                         )
        user_states.update_state(msg.chat.id, textdata.States.mail)


@bot.message_handler(func=lambda msg: user_states.is_current_state(
                msg.chat.id, textdata.States.mail
            )
)
def mail(msg):
    if msg.text == textdata.Buttons.back:
        backToMainmenu(msg)
        return

    data = table_users.mailing()
    for i in data:
        bot.send_message(i[0], msg.text)


if __name__ == "__main__":
    thread = threading.Thread(target=time_monitoring.observer, args=[bot])
    thread.start()
    bot.polling(timeout=5)
