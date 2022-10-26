import sqlite3
import re

def delete_customer(user):

    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    c.execute(f"DELETE from customers WHERE email = '{user}' ")

    conn.commit()
    conn.close()

def stitch_apart_for_databae_import(user):
    changed_username = user.replace("@", "_at_").replace(".", "_dot_")
    return changed_username

def stitch_back(user):
    changed_back = user.replace("_at_", "@").replace("_dot_", ".")

    return changed_back

def update_logged_in(user):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    c.execute(f"UPDATE last_signin SET users = '{user}' WHERE rowid = 1")

    conn.commit()
    conn.close()

def fetch_logged_in_user():
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM last_signin WHERE rowid = 1")

    user = c.fetchall()[0][1]

    conn.commit()
    conn.close()

    return user

def fetch_preferences(user):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    c.execute(f"SELECT * FROM {user}")

    preferences = c.fetchall()[0]

    conn.commit()
    conn.close()

    return preferences

def update_preferences_by_list(user, prefs_list):
    conn = sqlite3.connect('customers.db')
    c = conn.cursor()

    print(user + " wants to upload these " + str(prefs_list))
    c.execute(f"DELETE from {user} WHERE rowid = 1")

    c.execute(f"""INSERT INTO {user} VALUES (
        '{prefs_list[0]}',
        '{prefs_list[1]}',
        '{prefs_list[2]}',
        '{prefs_list[3]}',
        '{prefs_list[4]}',
        '{prefs_list[5]}',
        '{prefs_list[6]}',
        '{prefs_list[7]}',
        '{prefs_list[8]}'
    )""")

    conn.commit()
    conn.close()

