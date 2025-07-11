from classes.user import User
from datetime import datetime
from classes import Database

table_name = 'user'

def get_users() -> list[User]:
    # Read users from db
    db = Database()
    _, db_select_user_outputs = db.read(table_name)
    users =[]
    for db_select_user_output in  db_select_user_outputs:
        id, email_address, password, created_at = db_select_user_output
        users.append(User(id= int(id), email_address =str(email_address), password=str(password), created_at= datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S")))

    return users

def post_user(user_dict: dict) -> User:
    # Insert new user data
    db = Database()
    _, _ = db.insert(table_name, user_dict)
    
    # Read newly inserted user from db
    _, db_select_user_outputs = db.read(table_name, criteria=user_dict)
    id, email_address, password, created_at = db_select_user_outputs[-1]

    return User(id= int(id), email_address =str(email_address), password=str(password), created_at= datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S"))
