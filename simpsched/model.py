from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: str
    due_at: Optional[str]
