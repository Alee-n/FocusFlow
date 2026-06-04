import psycopg2
import os

def connect_db():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
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

        email TEXT UNIQUE,

        password_hash TEXT,

        role TEXT DEFAULT 'user'
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


def create_user(username, email, password_hash):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password_hash)

        VALUES (%s, %s, %s)
        """,
        (username, email, password_hash),
    )

    connection.commit()

    connection.close()

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

def get_user_by_username(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username = %s
        """,
        (username,),
    )

    user = cursor.fetchone()

    connection.close()

    return user

def get_user_by_email(email):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = %s
        """,
        (email,),
    )

    user = cursor.fetchone()

    connection.close()

    return user

def get_total_focus_time(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(SUM(time), 0)
        FROM sessions
        WHERE username = %s
        """,
        (username,),
    )

    total = cursor.fetchone()[0]

    connection.close()

    return total

def get_average_session_time(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COALESCE(AVG(time), 0)
        FROM sessions
        WHERE username = %s
        """,
        (username,),
    )

    average = cursor.fetchone()[0]

    connection.close()

    return round(float(average), 2)

def get_most_common_energy(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT energy
        FROM sessions
        WHERE username = %s
        GROUP BY energy
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """,
        (username,),
    )

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else "N/A"

def get_most_used_mode(username):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT mode
        FROM sessions
        WHERE username = %s
        GROUP BY mode
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """,
        (username,),
    )

    result = cursor.fetchone()

    connection.close()

    return result[0] if result else "N/A"