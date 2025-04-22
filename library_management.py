from book_db_management import *
from user_db_management import *
from constant import get_int, get_date, take_date
import datetime


user_collection = load_members_db()


class Member(User):
    def __init__(self, u_name, u_email, u_pass):
        super().__init__(u_name, u_email, u_pass)
        self.role = RoleStatus.member.value

    def borrow_book(self):
        show_books_db()
        print("Book ISBN: ")
        book_isbn = get_int()
        print("Borrow date (YYYY-DD-MM): ")
        borrow_date = get_date()
        book_collection = load_books_db()
        if book_isbn in book_collection:
            book = book_collection[book_isbn]
            if book.copies > 0:
                with database:
                    new_copies = book.copies - 1
                    c.execute(
                        "UPDATE books SET copies =:copies WHERE isbn =:isbn",
                        {"copies": new_copies, "isbn": book_isbn},
                    )
                borrow_book_db(self, book_isbn, borrow_date)
            else:
                with database:
                    c.execute(
                        "UPDATE books SET status =:status WHERE isbn =:isbn",
                        {"status": BookStatus.not_available.value, "isbn": book_isbn},
                    )
                print("No available book is present")
        else:
            print("Invalid ISBN")

    def return_book(self):
        show_books_db()
        print("Book ISBN: ")
        book_isbn = get_int()
        return_date = datetime.datetime.now()
        book_collection = load_books_db()

        book = book_collection[book_isbn]
        with database:
            new_copies = book.copies + 1
            c.execute(
                "UPDATE books SET copies =:copies WHERE isbn =:isbn",
                {"copies": new_copies, "isbn": book_isbn},
            )
        book = book_collection[book_isbn]
        return_book_db(self, book_isbn, return_date)


class Admin(User):
    def __init__(self, u_name, u_email, u_pass):
        super().__init__(u_name, u_email, u_pass)
        self.role = RoleStatus.admin.value

    def add_book(self):
        print("---ADDING BOOK---")
        title = input("Title: ")
        author = input("Author: ")
        genre = input("Genre: ")
        print("Copies: ")
        copies = get_int()
        book = Book(title, author, genre, copies)
        add_book_db(book)
        book_collection = load_books_db()

    def update_book(self):
        show_books_db()
        print("---UPDATING BOOK---")
        print("Book ISBN: ")
        isbn = get_int()
        title = input("Enter Title: ")
        print("Enter copies: ")
        copies = get_int()
        book_collection = load_books_db()
        if isbn in book_collection:
            update_book_db(isbn, title, copies)
            print("Book is successfully updated")

        else:
            print("Book doesn't exist in the library")

    def delete_book(self):
        show_books_db()
        print("---DELETING BOOK---")
        print("Book ISBN: ")
        isbn = get_int()
        book_collection = load_books_db()
        if isbn in book_collection:
            delete_book_db(isbn)
            print("Book is successfully deleted")
        else:
            print("Book doesn't exist in the library")

    def search_book(self):
        print("---SEARCHING BOOK---")
        title = input("Enter title: ")
        search_book_db(title)

    def add_member(self):
        name = input("Name :")
        email = input("Email: ")
        password = input("Password: ")
        user = User(name, email, password)
        user_collection = load_members_db()
        add_member_db(user)

    def update_member(self):
        show_members_db()
        print("---UPDATING USER---")
        print("Enter user id: ")
        u_id = get_int()
        name = input("Enter press or type user name: ")
        email = input("Enter press or type user email: ")
        password = input("Enter or press password :")
        user_collection = load_members_db()
        if u_id in user_collection:
            update_member_db(u_id, name, email, password)
            # ektu problem kore
            print("Successfully updated")
            print("After updation {}".format(user_collection[u_id]))
        else:
            print("User doesn't exist")

    def delete_member(self):
        show_members_db()
        print("---DELETING USER---")
        print("Enter user id: ")
        u_id = get_int()
        user_collection = load_members_db()
        if u_id in user_collection:
            delete_member_db(u_id)
            print("Deletion is successfull")
        else:
            print("User doesn't exist")
