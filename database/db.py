import psycopg2


def connect_db():

    connection = psycopg2.connect(
        host="localhost",
        database="focusflow",
        user="postgres",
        password="aleen003",
        port="5432",
    )

    return connection


def create_tables():

    connection = connect_db()

    cursor = connection.cursor()

    # ---------- USERS TABLE ----------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id SERIAL PRIMARY KEY,

            username TEXT UNIQUE,

            password TEXT
        )
        """)

    # ---------- SESSIONS TABLE ----------
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (

            id SERIAL PRIMARY KEY,

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

        VALUES (%s, %s)
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
        WHERE username = %s
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

        VALUES (%s, %s, %s, %s, %s)
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
        WHERE username = %s
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
        WHERE username = %s
        """,
        (username,),
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total
