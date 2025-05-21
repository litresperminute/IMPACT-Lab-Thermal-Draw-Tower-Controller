import re

def name_check(name: str):
    name = name.strip()
    if not re.fullmatch(r"[A-Za-z0-9 ()/]+", name):
        return False
    return True

def label_check(labe: str):
    label = label.strip()
    if not re.fullmatch(r"[A-Za-z0-9 ()/]+", label):
        return False
    return True

def int_check(number: str):
    number = number.strip()
    if number.startswith("-") or number.startswith("+") or not number.isdigit():
        return False
    return True