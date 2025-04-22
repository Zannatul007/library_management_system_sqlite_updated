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


def search_book_db(isbn=None, title=None):
    if isbn:
        with database:
            c.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
            book = c.fetchone()[0]
            isbn, title, author, genre, copies, status = book
            print(
                "ISBN :{}\nTitle : {}\nAuthor :{}\nGenre :{}\nCopies :{}\nStatus :{}".format(
                    isbn, title, author, genre, copies, status
                )
            )

    if title:
        with database:
            c.execute("SELECT * FROM books WHERE title = :title", {"title": title})
            book = c.fetchone()[0]
            isbn, title, author, genre, copies, status = book
            print(
                "ISBN :{}\nTitle : {}\nAuthor :{}\nGenre :{}\nCopies :{}\nStatus :{}".format(
                    isbn, title, author, genre, copies, status
                )
            )


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
                "ISBN :{}\nTitle : {}\nAuthor :{}\nGenre :{}\nCopies :{}\nStatus :{}".format(
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
      member_id INT NOT NULL,
      borrow_date TEXT,
      return_date TEXT,
      reserved BOOL,
      returned BOOL,
      FOREIGN KEY (book_isbn) REFERENCES books(isbn),
      FOREIGN KEY (member_id) REFERENCES members(id))"""
)


def borrow_book_db(user, book, borrow_date):

    with database:
        c.execute(
            "SELECT * FROM borrowed_books WHERE book_isbn =:book_isbn AND member_id=:member_id AND reserved = :reserved",
            {
                "book_isbn": book.isbn,
                "member_id": user.id,
                "reserved": False,
            },
        )
        row = c.fetchone()
        if row is None:
            c.execute(
                "INSERT INTO borrowed_books (book_isbn,member_id,borrow_date,return_date,reserved,returned) VALUES('book_isbn:',:member_id,:borrow_date,:reserved,:returned)",
                {
                    "book_isbn": book.isbn,
                    "member_id": user.id,
                    "borrow_date": borrow_date,
                    "reserved": True,
                    "returned": False,
                },
            )
        else:
            print("Book is already borrowed by you")


def return_book_db(user, book, return_date):

    with database:
        c.execute(
            "SELECT * FROM borrowed_books WHERE book_isbn =:book_isbn AND member_id=:member_id AND returned = :returned",
            {
                "book_isbn": book.isbn,
                "member_id": user.id,
                "returned": False,
            },
        )
        row = c.fetchone()
        if row is None:
            c.execute(
                "INSERT INTO borrowed_books (book_isbn,member_id,return_date,return_date,reserved,returned) VALUES('book_isbn:',:member_id,:return_date,:reserved,:returned)",
                {
                    "book_isbn": book.isbn,
                    "member_id": user.id,
                    "return_date": return_date,
                    "reserved": False,
                    "returned": True,
                },
            )
        else:
            print("Book is already returned by you")
