from library_management import *
import argon2
import sqlite3

database = sqlite3.connect("library_management.sqlite")
c = database.cursor()

hasher = argon2.PasswordHasher()


def get_hash(password):
    hashed_password = hasher.hash(password)
    return hashed_password


with database:
    c.execute("SELECT * FROM members WHERE admin = 1")
    admin = c.fetchone()
    if admin is None:
        name = "admin"
        email = "admin@gmail.com"
        password = "admin"
        h_password = get_hash(password)
        c.execute(
            "INSERT INTO members (password,name,email,admin) VALUES(:password,:name,:email,:admin)",
            {
                "password": h_password,
                "name": name,
                "email": email,
                "admin": True,
            },
        )
        admin1 = Admin(name, email, password)

        print(admin1.role)
        print("Default admin created")


def login():
    email = input("Email: ")
    password = input("Password: ")

    with database:
        c.execute(
            "SELECT * FROM members WHERE email = :email",
            {"email": email},
        )
        user_info = c.fetchone()
        if user_info:
            u_id, db_password, name, email, role = user_info
            print
            try:
                hasher.verify(db_password, password)
                print("Login is successful")
                if role:
                    new_user = Admin(name, email, password)
                    print(new_user)
                else:
                    new_user = Member(name, email, password)
                    print(new_user)
                return new_user
            except (
                argon2.exceptions.VerifyMismatchError
                or argon2.exceptions.InvalidHashError
            ):
                print("Invalid credentials. Please try again")
        else:
            print("Invalid credentials. Please try again!")
        return None


def register():
    name = input("Name: ")
    email = input("Email: ")
    password = input("Password: ")
    h_password = get_hash(password)
    # role = input("Role Member/Admin: ")

    with database:
        c.execute("SELECT * FROM members WHERE email = :email", {"email": email})
        user_info = c.fetchone()

        if user_info is None:
            c.execute(
                "INSERT INTO members (password,name,email,admin) VALUES(:password,:name,:email,:admin)",
                {
                    "password": h_password,
                    "name": name,
                    "email": email,
                    "admin": False,
                },
            )

            new_user = Member(name, email, password)
            new_user.id = c.lastrowid
            new_user.role = RoleStatus.member.value
            print("Registration is successful")
            return new_user

        else:
            print("User is already exist in the library")
            return None


# # print(load_members())

# u1 = register()
# # u1 = login()
