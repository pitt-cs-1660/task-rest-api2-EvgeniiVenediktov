############################################
# This file is used by the server.py file to connect to the database. Do not alter this file.
############################################
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
import sqlite3

# sqlite3 database file path
DATABASE_PATH = "./tasks.db"


def init_db():
    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                completed BOOLEAN NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()


# dependency injection is fun!
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


class DB:
    def __init__(self):
        init_db()
        self.conn = get_db_connection()
    
    def close(self):
        self.conn.close()

    def _insert_test_task(self) -> int:
        id = self.insert_task(TaskCreate(title="test", description="desc", completed=False))
        return id

    def insert_task(self, task_data: TaskCreate) -> int:
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)", 
            (task_data.title, task_data.description, task_data.completed),
        )
        id = cursor.lastrowid

        self.conn.commit()
        return id

    def does_task_exist(self, task_id: int) -> bool:
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT id FROM tasks WHERE id = ?", (task_id,)).fetchall()
        if len(rows) == 0:
            return False
        return True
    
    def get_tasks(self) -> list[TaskRead]:
        cursor = self.conn.cursor()
        tasks = []

        for row in cursor.execute("SELECT id, title, description, completed FROM tasks;"):
            tasks.append(TaskRead(id=row[0], title=row[1], description=row[2], completed=row[3]))
        return tasks
    
    def update_task(self, task_id:int, task_data: TaskCreate) -> TaskRead:
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE tasks SET (title, description, completed) = (?, ?, ?) WHERE id=?",
            (task_data.title,
            task_data.description,
            task_data.completed,
            task_id),    
        )

        self.conn.commit()
        return TaskRead(id=task_id, title=task_data.title, description=task_data.description, completed=task_data.completed)

    def delete_task(self, task_id: int):
        cursor = self.conn.cursor()
        result = cursor.execute(f"DELETE FROM tasks WHERE id={task_id};")
        self.conn.commit()
        return result.rowcount > 0