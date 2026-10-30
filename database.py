
import sqlite3

DB_NAME = "database.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lectures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            transcript TEXT NOT NULL,
            notes TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def save_lecture(title, transcript, notes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lectures (title, transcript, notes)
        VALUES (?, ?, ?)
    """, (title, transcript, notes))

    conn.commit()
    conn.close()


def get_all_lectures():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, created_at
        FROM lectures
        ORDER BY created_at DESC
    """)

    lectures = cursor.fetchall()
    conn.close()

    return lectures


def get_lecture(lecture_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM lectures WHERE id = ?
    """, (lecture_id,))

    lecture = cursor.fetchone()
    conn.close()

    return lecture


def update_lecture_notes(lecture_id, notes):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE lectures
        SET notes = ?
        WHERE id = ?
    """, (notes, lecture_id))

    conn.commit()
    conn.close()


def delete_lecture(lecture_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM lectures WHERE id = ?
    """, (lecture_id,))

    conn.commit()
    conn.close()


create_table()

