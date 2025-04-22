import datetime
import argon2

hasher = argon2.PasswordHasher()


def take_date(date):
    format = "%Y-%m-%d"
    x = datetime.datetime.strptime(date, format)
    return x


def get_hash(password):
    hashed_password = hasher.hash(password)
    return hashed_password


def get_int():
    while True:
        try:
            return int(input("> "))
        except ValueError:
            print("Invalid Number")


def get_date():
    while True:
        try:
            date = input()
            return take_date(date)
        except ValueError:
            print("Invalid time format")
