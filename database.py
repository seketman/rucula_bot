import os
import sqlite3
import time

database_file = 'data/rucula_data.db'

def get_connection():
    file_already_exist = os.path.isfile(database_file)
    connection = sqlite3.connect(database_file)
    if not file_already_exist:
        connection.execute('''CREATE TABLE "suscribers" (
            "id"							TEXT,
            "name"							TEXT,
            "gap"							INTEGER,
            "last_notified_value"			INTEGER,
            "last_notification_timestamp"	REAL,
            PRIMARY KEY("id")
        )''')
    return connection

def add_suscriber(connection, id, name, gap):
    return connection.execute("INSERT INTO suscribers (id, name, gap) VALUES (?, ?, ?)", (id, name, gap))

def get_suscribers(connection):
    connection.row_factory = sqlite3.Row 
    cursor = connection.cursor()
    return cursor.execute("SELECT id, name, gap, last_notified_value FROM suscribers")

def update_suscriber_gap(connection, id, gap):
    cursor = connection.cursor()
    cursor.execute("UPDATE suscribers SET gap = ? WHERE id = ?", (gap, id))
    connection.commit()

def update_suscriber_notification(connection, id, last_notified_value):
    cursor = connection.cursor()
    cursor.execute("UPDATE suscribers SET last_notified_value = ?, last_notification_timestamp = ? WHERE id = ?", (last_notified_value, time.time(), id))
    connection.commit()
