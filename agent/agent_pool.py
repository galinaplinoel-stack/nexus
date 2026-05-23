"""Agent pool management with auto-scaling."""
import asyncio
from .core import Agent, AgentConfig, AgentStatus


class AgentPool:
    """Manages a pool of agents with health monitoring and auto-scaling."""

    def __init__(self, min_agents: int = 1, max_agents: int = 10):
        self.agents: dict[str, Agent] = {}
        self.min_agents = min_agents
        self.max_agents = max_agents
        self._health_task = None

    def add_agent(self, config: AgentConfig) -> Agent:
        agent = Agent(config)
        self.agents[agent.agent_id] = agent
        return agent

    def remove_agent(self, agent_id: str):
        self.agents.pop(agent_id, None)

    def get_idle_agents(self) -> list[Agent]:
        return [a for a in self.agents.values() if a.status == AgentStatus.IDLE]

    def get_health_report(self) -> list[dict]:
        return [a.health_check() for a in self.agents.values()]

    def total_load(self) -> int:
        return sum(len(a.active_tasks) for a in self.agents.values())

    async def auto_scale(self, config: AgentConfig):
        """Scale pool based on current load."""
        idle = len(self.get_idle_agents())
        busy_count = sum(1 for a in self.agents.values() if a.status == AgentStatus.BUSY)

        if idle == 0 and len(self.agents) < self.max_agents:
            self.add_agent(config)
        elif idle > 2 and len(self.agents) > self.min_agents:
            for agent in self.get_idle_agents()[1:]:
                self.remove_agent(agent.agent_id)
                break

    def __len__(self):
        return len(self.agents)

    def __repr__(self):
        return f"AgentPool(size={len(self)}, load={self.total_load()})"
