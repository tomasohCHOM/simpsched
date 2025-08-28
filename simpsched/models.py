from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    desc: str
    status: str
    created_at: str
    updated_at: str
    due_at: Optional[str]
