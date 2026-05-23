"""NEXUS - AI Agent Orchestration Platform"""
from agent import Agent, Orchestrator, AgentPool
from agent.core import AgentConfig, Task


def main():
    print("=" * 50)
    print("  NEXUS - AI Agent Orchestration Platform")
    print("=" * 50)

    pool = AgentPool(min_agents=2, max_agents=10)
    orchestrator = Orchestrator()

    for i in range(3):
        config = AgentConfig(name=f"agent-{i}", agent_type="general")
        agent = pool.add_agent(config)
        orchestrator.add_agent(agent, ["general", "nlp", "vision"])

    print(f"\n✓ Initialized {len(pool)} agents")
    print(f"✓ Orchestrator ready with {len(orchestrator.router.routes)} routes")
    print(f"✓ System ready\n")


if __name__ == "__main__":
    main()
