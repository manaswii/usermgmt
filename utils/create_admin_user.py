from database import *

username = input("Enter username: ")
pass1 = input("Enter password: ")
pass2 = input("Enter password again: ")

if len(username) < 5 or len(pass1) < 5:
    print("They should be at least 5 characters")
elif pass1 != pass2:
    print("password don't match")
else:
    insert_into_admin(username=username, password=pass1)
