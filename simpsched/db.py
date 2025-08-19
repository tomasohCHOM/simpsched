import sqlite3
from typing import List, Optional, Tuple


class DatabaseHandler:
    _instance: Optional["DatabaseHandler"] = None
    conn: sqlite3.Connection
    cur: sqlite3.Cursor

    def __new__(cls, db_path: str = "tasks.db") -> "DatabaseHandler":
        if cls._instance == None:
            cls._instance = super().__new__(cls)
            cls._instance.conn = sqlite3.connect(db_path)
            cls._instance.cur = cls._instance.conn.cursor()
            cls._instance._setup()
        return cls._instance

    def _setup(self) -> None:
        self.cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                description TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
                due_at      TEXT
            )
        """
        )
        self.conn.commit()

    def add_task(
        self, title: str, description: str, due_at: Optional[str] = None
    ) -> None:
        """Insert a new task. `due_at` should be ISO string (YYYY-MM-DD HH:MM:SS) or None."""
        self.cur.execute(
            "INSERT INTO tasks (title, description, due_at) VALUES (?, ?, ?)",
            (title, description, due_at),
        )
        self.conn.commit()

    def remove_task(self, task_id: int) -> None:
        """Remove a task from the db with its corresponding `task_id`."""
        self.cur.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def update_status(self, task_id: int, status: str) -> None:
        """Update the status of a task with its corresponding `task_id`."""
        self.cur.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        self.conn.commit()

    def update_due_at(self, task_id: int, due_at: str) -> None:
        """Update due date. `due_at` should be in ISO string (YYYY-MM-DD HH:MM:SS) format."""
        self.cur.execute("UPDATE tasks SET due_at = ? WHERE id = ?", (due_at, task_id))
        self.conn.commit()

    def list_tasks(self) -> List[Tuple[int, str, str, str, str, Optional[str]]]:
        """Return (id, title, description, status, created_at, due_at) of each task in the db."""
        self.cur.execute(
            "SELECT id, title, description, status, created_at, due_at FROM tasks"
        )
        return self.cur.fetchall()

    def close(self) -> None:
        self.conn.close()
        DatabaseHandler._instance = None
