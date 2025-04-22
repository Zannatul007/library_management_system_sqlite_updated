import sqlite3
from enum import Enum


database = sqlite3.connect("library_management.sqlite")
c = database.cursor()
c.execute(
    """CREATE TABLE IF NOT EXISTS books (
    isbn INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT ,
    author TEXT ,
    genre TEXT ,
    copies INT ,
    status TEXT )"""
)


class BookStatus(Enum):
    reserved = "Reserved"
    returned = "Returned"
    available = "Available"
    not_available = "Not Available"


class Book:

    def __init__(self, title, author, genre, no_copies: int, isbn=None):
        self.isbn = None
        self.title = title
        self.author = author
        self.genre = genre
        self.copies = no_copies
        self.status = BookStatus.available.value

    def __str__(self):
        return " ISBN:{}\n Title: {}\n Author: {}\n Genre: {}\n Copies: {}\n Status: {}".format(
            self.isbn, self.title, self.author, self.genre, self.copies, self.status
        )


def add_book_db(book):
    with database:
        c.execute(
            "INSERT INTO books (title,author,genre,copies,status) VALUES (:title,:author,:genre,:copies,:status)",
            {
                "title": book.title,
                "author": book.author,
                "genre": book.genre,
                "copies": book.copies,
                "status": BookStatus.available.value,
            },
        )

        book.isbn = c.lastrowid


def update_book_db(isbn, title, copies):

    with database:
        c.execute(
            "UPDATE books SET title = :title,copies =:copies WHERE isbn= :isbn",
            {"title": title, "copies": copies, "isbn": isbn},
        )


def search_book_db(title):
    with database:
        c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
        book = c.fetchone()
        if book:
            isbn, title, author, genre, copies, status = book
            print(
                "ISBN :{}\nTitle : {}\nAuthor :{}\nGenre :{}\nCopies :{}\nStatus :{}".format(
                    isbn, title, author, genre, copies, status
                )
            )
        else:
            print("No book is found with this title")


def delete_book_db(isbn):
    with database:
        c.execute("DELETE FROM books WHERE isbn = :isbn", {"isbn": isbn})


def show_books_db():
    with database:
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        print("-" * 20)
        for book in books:
            isbn, title, author, genre, copies, status = book
            print(
                "ISBN : {}\nTitle : {}\nAuthor :{}\nGenre :{}\nCopies :{}\nStatus :{}".format(
                    isbn, title, author, genre, copies, status
                )
            )
            print("-" * 20)


book_collection = {}


def load_books_db():
    with database:
        c.execute("SELECT * FROM books")
        books = c.fetchall()
        for book in books:
            isbn_db, title, author, genre, copies, status = book
            new_book = Book(title, author, genre, copies)
            book_collection[isbn_db] = new_book
        return book_collection


c.execute(
    """CREATE TABLE IF NOT EXISTS borrowed_books(
      book_isbn INT NOT NULL,
      member_email TEXT NOT NULL,
      borrow_date TEXT,
      return_date TEXT,
      reserved BOOL,
      returned BOOL,
      FOREIGN KEY (book_isbn) REFERENCES books(isbn),
      FOREIGN KEY (member_email) REFERENCES members(email))"""
)


def borrow_book_db(user, isbn, borrow_date):
    with database:

        c.execute(
            "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_email = :member_email AND returned = 0",
            {
                "book_isbn": isbn,
                "member_email": user.email,
            },
        )
        row = c.fetchone()
        if row:
            print("Book is already borrowed by you")
        else:

            c.execute(
                "INSERT INTO borrowed_books (book_isbn, member_email, borrow_date, reserved, returned) VALUES (:book_isbn, :member_email, :borrow_date, :reserved, :returned)",
                {
                    "book_isbn": isbn,
                    "member_email": user.email,
                    "borrow_date": borrow_date,
                    "reserved": 1,
                    "returned": 0,
                },
            )


def return_book_db(user, isbn, return_date):
    with database:

        c.execute(
            "SELECT * FROM borrowed_books WHERE book_isbn = :book_isbn AND member_email = :member_email AND returned = :returned",
            {
                "book_isbn": isbn,
                "member_email": user.email,
                "returned": 0,
            },
        )
        row = c.fetchone()
        if row is None:
            print("You haven't borrowed this book or it's already returned")
        else:

            c.execute(
                "UPDATE borrowed_books SET return_date = :return_date, reserved = :reserved, returned = :returned WHERE book_isbn = :book_isbn AND member_email = :member_email AND returned = 0",
                {
                    "book_isbn": isbn,
                    "member_email": user.email,
                    "return_date": return_date,
                    "reserved": 0,
                    "returned": 1,
                },
            )


def show_all_transactions():
    with database:
        c.execute("SELECT * FROM borrowed_books")
        books = c.fetchall()
        for book in books:
            isbn, email, b_date, r_date, reserved, returned = book
            print(
                f"Isbn: {isbn}\nEmail: {email}\nBorrow Date: {b_date}\nReturn Date: {r_date}\nReserved: {reserved}\nReturned: {returned}"
            )


def show_books():
    book_collection = load_books_db()
    for isbn, book in book_collection.items():
        print(isbn)
        print(book)


show_books()
