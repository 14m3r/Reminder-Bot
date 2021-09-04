import re


def time(vvod):
    date = re.compile(
        r"^[0-2][0-9]:[0-5][0-9] 202[1-9]\-[0-1][0-9]\-[0-3][0-9]$"
    )
    time = re.compile(r"^[0-2][0-9]:[0-5][0-9]$")
    if re.search(date, vvod):
        return True, 1
    elif re.search(time, vvod):
        return True, 2
    return False, 0

