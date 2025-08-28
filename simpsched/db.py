import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from .models import Task


def get_db_path() -> Path:
    cwd = Path.cwd() / "task.db"
    if cwd.exists():
        return cwd
    home = Path.home() / ".local" / "share" / "simpsched" / "task.db"
    home.parent.mkdir(parents=True, exist_ok=True)
    return home


class DatabaseHandler:
    _instance: Optional["DatabaseHandler"] = None
    conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __new__(cls) -> "DatabaseHandler":
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(str(get_db_path()))
            cls._instance.cur = cls._instance.conn.cursor()
            cls._instance._setup()
        return cls._instance

    def _setup(self) -> None:
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                desc        TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
                due_at      TEXT,
                updated_at  TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        self.conn.commit()

    def get_task(self, task_id: int) -> Optional[int]:
        """Gets the task by its corresponding `task_id`."""
        self.cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        return self.cur.fetchone()

    def add_task(self, title: str, desc: str, status: str, due_at: str) -> None:
        """Insert a new task. `due_at` should be ISO string (YYYY-MM-DD HH:MM:SS) or None."""
        curr_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cur.execute(
            "INSERT INTO tasks (title, desc, status, created_at, due_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
            (title, desc, status, curr_time, due_at, curr_time),
        )
        self.conn.commit()

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the db with its corresponding `task_id`."""
        self.cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def update_task(self, task_id: int, **updates) -> None:
        """Updates a task with its `task_id` based on the provided fields."""
        if not updates:
            return
        set_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        values = list(updates.values()) + [task_id]
        self.cur.execute(f"UPDATE tasks SET {set_clause} WHERE id = ?", values)
        self.conn.commit()

    def list_tasks(self) -> List[Task]:
        """Return list of Task objects from the db."""
        self.cur.execute(
            "SELECT id, title, desc, status, created_at, updated_at, due_at FROM tasks"
        )
        rows = self.cur.fetchall()
        return [Task(*row) for row in rows]

    def close(self) -> None:
        self.conn.close()
        DatabaseHandler._instance = None
