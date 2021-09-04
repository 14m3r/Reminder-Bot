import datetime
from time import sleep
import lib.db_work

table = lib.db_work.RemindersTable()


def getdatetime(vvod, option):
    if option == 1:
        d_object = datetime.datetime.strptime(vvod, '%Y-%mm-%dd %H:%M')
    elif option == 2:
        now = datetime.datetime.now().date().strftime('%Y-%mm-%dd')
        vvod = f"{now} {vvod}"
        d_object = datetime.datetime.strptime(vvod, '%Y-%mm-%dd %H:%M')
    return d_object


def observer(bot):
    while True:
        sleep(10)
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')
        reminds = table.getrems()
        for remind in reminds:
            print(remind, now)
            if remind[3] == now:
                bot.send_message(remind[1], remind[2])
                table.delrems(remind[0])
