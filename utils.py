import sqlite3
import os


if not __name__ == '__main__':
    if not os.path.isfile("users.db"):  # initializing the database if it doesn't exist
        _conn = sqlite3.connect("users.db")
        _cursor = _conn.cursor()
        _cursor.execute("CREATE TABLE IF NOT EXISTS users(STRING username, INTEGER kills, INTEGER deaths)")
        _conn.commit()
        _conn.close()


def get_user_data(username: str) -> tuple | None:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE username = ?""", (username,))
    selection = cursor.fetchone()
    return selection


def save_user_data(username: str, data: tuple[int, int]) -> None:
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", username)
    fetched = cursor.fetchone()
    if fetched != () and fetched is not None:
        _, kills, deaths = fetched
        kills += data[0]
        deaths += data[1]
        final_data = (_, kills, deaths)
    else:
        final_data = (username, data[0], data[1])
    cursor.execute("INSERT INTO users WHERE username = ? VALUES(?)", final_data)
