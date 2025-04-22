import sqlite3
from enum import Enum

import argon2


hasher = argon2.PasswordHasher()


def get_hash(password):
    hashed_password = hasher.hash(password)
    return hashed_password


class RoleStatus(Enum):
    admin = "Admin"
    member = "Member"


database = sqlite3.connect("library_management.sqlite")
c = database.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS members(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    admin BOOL)"""
)

user_collection = {}


class User:
    def __init__(self, u_name, u_email, u_pass):
        self.id = None
        self.name = u_name
        self.email = u_email
        self.password = u_pass
        self.role = None

    def __str__(self):
        return "Name: {}\n Email: {}\n Role: {}".format(
            self.name, self.email, self.role
        )


def add_member_db(user):
    with database:
        c.execute(
            "INSERT INTO members (name,email,password,admin) VALUES (:name,:email,:password,:admin)",
            {
                "name": user.name,
                "email": user.email,
                "password": get_hash(user.password),
                "admin": False,
            },
        )

        user.role = RoleStatus.member.value
        

        user.id = c.lastrowid


def update_member_db(u_id, name=None, email=None, password=None):
    if name:
        with database:
            c.execute(
                "UPDATE members SET name= :name WHERE id= :id",
                {"name": name, "id": u_id},
            )
    if email:
        with database:
            c.execute(
                "UPDATE members SET email= :email WHERE id= :id",
                {"email": email, "id": u_id},
            )
    if password:
        with database:
            c.execute(
                "UPDATE members SET password= :password WHERE id= :id",
                {"password": password, "id": u_id},
            )


def delete_member_db(u_id):
    with database:
        c.execute("DELETE FROM members WHERE id = :id", {"id": u_id})


def show_members_db():
    with database:
        c.execute("SELECT * FROM members")
        members = c.fetchall()
        for member in members:
            m_id, password, name, email, admin = member
            role = ""
            if admin == 1:
                role = "Admin"
            else:
                role = "Member"
            print(
                "ID: {}\nName: {}\nEmail: {}\nRole:{}".format(m_id, name, email, role)
            )


def load_members_db():
    with database:
        c.execute("SELECT * FROM members")
        members = c.fetchall()
        for member in members:
            m_id, password, name, email, admin = member
            new_member = User(name, email, password)
            if admin == 0:
                new_member.role = RoleStatus.member.value
            else:
                new_member.role = RoleStatus.admin.value

            user_collection[m_id] = new_member
        return user_collection
