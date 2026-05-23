"""NEXUS CLI - Command line interface for agent orchestration."""
import argparse
import asyncio
from agent import Orchestrator, AgentPool
from agent.core import AgentConfig, Task


def cmd_status(args):
    pool = AgentPool()
    print(f"NEXUS Status: ONLINE")
    print(f"Agents: {len(pool)}")
    print(f"Queue: 0 pending")


def cmd_submit(args):
    print(f"Task submitted: {args.task}")
    print(f"Routed to: agent-0 (general)")


def cmd_agents(args):
    print("Agent ID    | Name      | Status | Tasks")
    print("-" * 48)
    print("a1b2c3d4    | agent-0   | idle   | 0")
    print("e5f6g7h8    | agent-1   | idle   | 0")
    print("i9j0k1l2    | agent-2   | idle   | 0")


def main():
    parser = argparse.ArgumentParser(description="NEXUS CLI - AI Agent Orchestration")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("status", help="Show system status")
    p_submit = sub.add_parser("submit", help="Submit a task")
    p_submit.add_argument("task", help="Task description")
    sub.add_parser("agents", help="List all agents")

    args = parser.parse_args()
    {"status": cmd_status, "submit": cmd_submit, "agents": cmd_agents}.get(
        args.command, lambda a: parser.print_help()
    )(args)


if __name__ == "__main__":
    main()
