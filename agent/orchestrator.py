"""Task orchestrator for routing and scheduling."""
import asyncio
from collections import defaultdict
from .core import Agent, Task, AgentStatus


class TaskRouter:
    """Routes tasks to appropriate agents based on type and priority."""

    def __init__(self):
        self.routes: dict[str, list[str]] = defaultdict(list)

    def register_route(self, task_type: str, agent_id: str):
        self.routes[task_type].append(agent_id)

    def resolve(self, task_type: str, agents: dict[str, Agent]) -> Agent | None:
        candidates = self.routes.get(task_type, [])
        best, best_load = None, float("inf")
        for aid in candidates:
            if aid in agents and agents[aid].status != AgentStatus.OFFLINE:
                load = len(agents[aid].active_tasks)
                if load < best_load:
                    best, best_load = agents[aid], load
        return best


class Orchestrator:
    """Orchestrates task distribution across agents."""

    def __init__(self):
        self.router = TaskRouter()
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        self.results: dict[str, Task] = {}
        self._running = False

    def add_agent(self, agent: Agent, task_types: list[str]):
        """Register an agent for specific task types."""
        for t in task_types:
            self.router.register_route(t, agent.agent_id)

    async def submit(self, task: Task):
        """Submit a task to the queue."""
        await self.task_queue.put((task.priority, task))

    async def dispatch(self, agents: dict[str, Agent]):
        """Dispatch next task from queue to best agent."""
        if self.task_queue.empty():
            return None
        _, task = await self.task_queue.get()
        agent = self.router.resolve(task.payload.get("type", "general"), agents)
        if agent:
            result = await agent.execute(task)
            self.results[task.task_id] = task
            return result
        else:
            await self.task_queue.put((task.priority, task))
            return None

    def get_stats(self) -> dict:
        return {
            "queued": self.task_queue.qsize(),
            "completed": len(self.results),
            "routes": len(self.router.routes),
        }
