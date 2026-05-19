import sqlite3


def connect_db():

    connection = sqlite3.connect("focusflow.db")

    return connection


def create_tables():

    connection = connect_db()

    cursor = connection.cursor()

    # ---------- USERS TABLE ----------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT UNIQUE,

            password TEXT
        )
        """)

    # ---------- SESSIONS TABLE ----------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            username TEXT,

            task TEXT,

            time INTEGER,

            energy TEXT,

            mode TEXT
        )
        """)

    connection.commit()

    connection.close()


# ---------- USER FUNCTIONS ----------


def create_user(username, password):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (username, password)

        VALUES (?, ?)
        """,
        (username, password),
    )

    connection.commit()

    connection.close()


def get_user(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT * FROM users
        WHERE username = ?
        """,
        (username,),
    )

    user = cursor.fetchone()

    connection.close()

    return user


# ---------- SESSION FUNCTIONS ----------


def save_session(username, task, time, energy, mode):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO sessions
        (username, task, time, energy, mode)

        VALUES (?, ?, ?, ?, ?)
        """,
        (username, task, time, energy, mode),
    )

    connection.commit()

    connection.close()


def get_total_sessions():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM sessions")

    total = cursor.fetchone()[0]

    connection.close()

    return total


def get_user_sessions(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT task, time, energy, mode
        FROM sessions
        WHERE username = ?
        """,
        (username,),
    )

    sessions = cursor.fetchall()

    connection.close()

    return sessions


def get_user_total_sessions(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM sessions
        WHERE username = ?
        """,
        (username,),
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total
