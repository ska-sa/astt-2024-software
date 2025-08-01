from datetime import datetime
import os
from dotenv import load_dotenv, set_key
import sqlite3
import fastapi

class Database:
    def __init__(self) -> None:
        load_dotenv()
        env = os.getenv('ENV', 'development')
        self.name = f"databases/{env}.db"
        self.conn = sqlite3.connect(self.name, check_same_thread=False)
        self.cur = self.conn.cursor()
        self.create_tables()

    def create_tables(self) -> None:
        self.cur.executescript("""
            CREATE TABLE IF NOT EXISTS user(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `email_address` TEXT UNIQUE,
                `password` TEXT,
                `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS telescope(
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` TEXT UNIQUE,
                `health_status` TEXT,
                `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP
            );                   
        """)
        self.conn.commit()

    def insert(self, table_name: str, data: dict) -> tuple[bool, list]:
        try:
            columns = ', '.join([f"`{key}`" for key in data.keys()])
            placeholders = ', '.join(['?' for _ in data])
            sql = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
            self.cur.execute(sql, list(data.values()))
            self.conn.commit()
            return (True, [data])
        except sqlite3.IntegrityError as e:
            print(f"Error inserting data: {e}")
            return (False, [])

    def delete(self, table_name: str, criteria: dict) -> tuple[bool, list]:
        try:
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria])
            sql = f"DELETE FROM `{table_name}` WHERE {where_clause}"
            self.cur.execute(sql, list(criteria.values()))
            self.conn.commit()
            return (True, [criteria])
        except sqlite3.Error as e:
            print(f"Error deleting data: {e}")
            return (False, [])

    def read(self, table_name: str, criteria: dict = None, limit: int = None, offset: int = None) -> tuple[bool, list]:
        try:
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria]) if criteria else ""
            limit_clause = f"LIMIT {limit}" if limit else ""
            offset_clause = f"OFFSET {offset}" if offset else ""
            sql = f"SELECT * FROM `{table_name}` " + \
                  (f"WHERE {where_clause} " if where_clause else "") + \
                  (f"{limit_clause} " if limit_clause else "") + \
                  (f"{offset_clause}" if offset_clause else "")
            self.cur.execute(sql, list(criteria.values()) if criteria else [])
            return (True, self.cur.fetchall())
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return (False, [])

    def read_range(self, table_name: str, min_id: int, max_id: int) -> tuple[bool, list]:
        try:
            sql = f"SELECT * FROM `{table_name}` WHERE `id` BETWEEN ? AND ?"
            self.cur.execute(sql, (min_id, max_id))
            return (True, self.cur.fetchall())
        except sqlite3.Error as e:
            print(f"Error reading data: {e}")
            return (False, [])

    def update(self, table_name: str, data: dict, criteria: dict) -> tuple[bool, list]:
        try:
            set_clause = ', '.join([f"`{key}` = ?" for key in data])
            where_clause = ' AND '.join([f"`{key}` = ?" for key in criteria])
            sql = f"UPDATE `{table_name}` SET {set_clause} WHERE {where_clause}"
            self.cur.execute(sql, list(data.values()) + list(criteria.values()))
            self.conn.commit()
            return (True, [data])
        except sqlite3.Error as e:
            print(f"Error updating data: {e}")
            return (False, [])

    def clear(self) -> tuple[bool, list]:
        if self.name not in ['production', 'development']:
            try:
                # Drop all tables
                self.cur.executescript("""
                    DROP TABLE IF EXISTS `user`;
                """)
                self.conn.commit()
                # Recreate tables
                self.create_tables()
                return (True, [])
            except sqlite3.Error as e:
                print(f"Error clearing the database: {e}")
                return (False, [])
        return (False, [])

def main() -> None:
    from user import User
    #load_dotenv()
    #set_key("", "testing")
    db = Database()
    print()

    # Insert new data
    db_insert_status, db_insert_output = db.insert('user', {'email_address': 'shlabisa@sa', 'password': 'pass'})
    print("Insert", db_insert_status, db_insert_output)
    print()
    
    # Read users from db
    db_read_status, db_read_output = db.read('user')
    print("Read", db_read_status, db_read_output)
    print(*db_read_output[0])
    id, email_address, password, created_at = db_read_output[0]
    print(User(id=1,
                email_address="snyide@gmail.com",
                password="snyide",
                created_at=datetime.now()))
    user = User(id= int(id), email_address =str(email_address), password=str(password), created_at= datetime.strptime(str(created_at), "%Y-%m-%d %H:%M:%S"))

    # Update user
    user_dict: dict = user.__dict__
    user_dict["password"] = "pass-updated"
    db_update_status, db_update_output = db.update('user', user_dict, {'id': user.id})
    print("Update", db_update_status, db_update_output)
    print()
    
    db_delete_status, db_delete_output = db.delete('user', {'id': user.id})
    print("Delete", db_delete_status, db_delete_output)
    print()

# Example usage:
if __name__ == "__main__":
    main()