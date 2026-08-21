import sqlite3

def init_db():
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    """)
    conn.commit()
    conn.close()

def add_task(user_id: int, task_text: str):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (user_id, task_text))
    conn.commit()
    conn.close()

def get_tasks(user_id: int):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, status FROM tasks WHERE user_id = ? AND status = 'pending'", (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def complete_task(task_id: int, user_id: int):
    conn = sqlite3.connect("todo.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET status = 'done' WHERE id = ? AND user_id = ?", (task_id, user_id))
    conn.commit()
    conn.close()