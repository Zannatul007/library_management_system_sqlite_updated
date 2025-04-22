from auth import *
from constant import *

while True:
    print("1. Login")
    print("2. Register")
    print("3. Exit")
    print("SELECT Option from 1 to 3")
    ip1 = get_int()
    if ip1 == 1:
        user = login()
        if user.role == "Member":
            while True:
                print("1. Borrow book")
                print("2. Return book")
                print("3. show transaction")
                print("4. Logout")
                print("SELECT Option from 1 to 4")
                ip2 = get_int()
                if ip2 == 1:
                    user.borrow_book()
                if ip2 == 2:
                    user.return_book()
                if ip2 == 3:
                    pass
                if ip2 == 4:
                    break
        elif user.role == "Admin":
            while True:
                print("1: Add book")
                print("2: Remove Book")
                print("3: Update Book")
                print("4: Search Book")
                print("5: Add User")
                print("6: Remove User")
                print("7: Update User")
                print("8: Usage Report")
                print("9: Show books")
                print("10: Show member")
                print("11: Logout")
                print("SELECT Option from 1 to 11")
                ip3 = get_int()
                if ip3 == 1:
                    user.add_book()
                if ip3 == 2:
                    user.delete_book()
                if ip3 == 3:
                    user.update_book()
                if ip3 == 4:
                    user.search_book()
                if ip3 == 5:
                    user.add_member()
                if ip3 == 6:
                    user.delete_member()
                if ip3 == 7:
                    user.update_member
                if ip3 == 8:
                    pass
                if ip3 == 9:
                    show_books_db()
                if ip3 == 10:
                    show_members_db()
                if ip3 == 11:
                    break
