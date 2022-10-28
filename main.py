from mysql_connection.mysql_connection import * 
from user_class import *

print("********** WELCOME **********")
print("1. Login\n2. SignUp")
first_input = int(input("please select: "))

if first_input == 1:
    user_login.login()
elif first_input == 2:
    user_register.register()