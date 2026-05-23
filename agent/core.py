"""Core Agent module for NEXUS."""
import uuid
import asyncio
from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Callable, Optional


class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"


@dataclass
class AgentConfig:
    name: str
    agent_type: str = "general"
    max_concurrent_tasks: int = 5
    timeout: float = 300.0
    retry_count: int = 3


@dataclass
class Task:
    task_id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    payload: dict = field(default_factory=dict)
    priority: int = 0
    callback: Optional[Callable] = None
    result: Any = None
    status: str = "pending"


class Agent:
    """Core AI agent that processes tasks."""

    def __init__(self, config: AgentConfig):
        self.agent_id = str(uuid.uuid4())[:8]
        self.config = config
        self.status = AgentStatus.IDLE
        self.active_tasks: dict[str, Task] = {}
        self.completed_tasks: int = 0
        self.failed_tasks: int = 0

    async def execute(self, task: Task) -> Any:
        """Execute a task."""
        if len(self.active_tasks) >= self.config.max_concurrent_tasks:
            raise RuntimeError(f"Agent {self.agent_id} at max capacity")

        self.status = AgentStatus.BUSY
        self.active_tasks[task.task_id] = task
        task.status = "running"

        try:
            await asyncio.sleep(0.1)  # Simulated work
            task.result = {"status": "completed", "agent": self.agent_id}
            task.status = "completed"
            self.completed_tasks += 1
        except Exception as e:
            task.status = "failed"
            self.failed_tasks += 1
            raise
        finally:
            del self.active_tasks[task.task_id]
            if not self.active_tasks:
                self.status = AgentStatus.IDLE

        return task.result

    def health_check(self) -> dict:
        """Return agent health status."""
        return {
            "agent_id": self.agent_id,
            "name": self.config.name,
            "type": self.config.agent_type,
            "status": self.status.value,
            "active_tasks": len(self.active_tasks),
            "completed": self.completed_tasks,
            "failed": self.failed_tasks,
        }

    def __repr__(self):
        return f"Agent({self.config.name}, status={self.status.value})"
