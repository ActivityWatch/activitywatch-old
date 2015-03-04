
import logging
from .base import Agent, Logger, Watcher
from .settings import Singleton


@Singleton
class ModuleManager():
    _agents = []

    def __init__(self):
        pass

    def add_agent(self, agent: Agent):
        if not isinstance(agent, Agent):
            raise Exception("'{}' is not an agent")

        if agent not in self._agents:
            self._agents.append(agent)
        else:
            logging.warning("Agent '{}' already added to the module manager".format(agent))

    def get_agents(self) -> "list[Agent]":
        # TODO: Make a property
        return self._agents

    """Starts loggers first, then filters, then watchers"""
    def start_agents(self):
        loggers = filter(lambda x: isinstance(x, Logger), self._agents)
        filters = filter(lambda x: isinstance(x, Logger) and isinstance(x, Watcher), self._agents)
        watchers = filter(lambda x: isinstance(x, Watcher), self._agents)
        self._start_agents(loggers)
        self._start_agents(filters)
        self._start_agents(watchers)

    """Starts a list of agents after checking for each of them that they haven't already been started"""
    @staticmethod
    def _start_agents(agents: "list[Agent]"):
        for agent in agents:
            if not agent.is_alive():
                agent.start()
