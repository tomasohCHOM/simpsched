import sqlite3
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Task:
    id: int
    title: str
    desc: str
    status: str
    created_at: str
    due_at: Optional[str]


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
                desc TEXT,
                status      TEXT DEFAULT 'pending',
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP,
                due_at      TEXT
            )
        """
        )
        self.conn.commit()

    def get_task(self, task_id: int) -> Optional[int]:
        """Gets the task by its corresponding `task_id`."""
        self.cur.execute("SELECT id FROM tasks WHERE id = ?", (task_id,))
        return self.cur.fetchone()

    def add_task(
        self, title: str, desc: str, status: str, due_at: Optional[str]
    ) -> None:
        """Insert a new task. `due_at` should be ISO string (YYYY-MM-DD HH:MM:SS) or None."""
        self.cur.execute(
            "INSERT INTO tasks (title, desc, status, due_at) VALUES (?, ?, ?, ?)",
            (title, desc, status, due_at),
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
            "SELECT id, title, desc, status, created_at, due_at FROM tasks"
        )
        rows = self.cur.fetchall()
        return [Task(*row) for row in rows]

    def close(self) -> None:
        self.conn.close()
        DatabaseHandler._instance = None
