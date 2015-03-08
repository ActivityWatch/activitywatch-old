from datetime import datetime
import logging

from .base import Agent, Logger, Watcher
from .settings import Singleton


@Singleton
class ModuleManager():
    _agents = []
    _started = None

    def __init__(self):
        self._started = datetime.now()

    def add_agent(self, agent: Agent):
        if not isinstance(agent, Agent):
            raise Exception("'{}' is not an agent")

        if agent not in self._agents:
            self._agents.append(agent)
        else:
            logging.warning("Agent '{}' already added to the module manager".format(agent))

    def add_agents(self, agents: "list[Agent]"):
        for agent in agents:
            self.add_agent(agent)

    @property
    def agents(self) -> "list[Agent]":
        return self._agents

    def _get_by_agent_type(self, agent_type) -> "list[Agent]":
        return list(filter(lambda x: x.agent_type == agent_type, self.agents))

    @property
    def loggers(self) -> "list[Logger]":
        return self._get_by_agent_type("logger")

    @property
    def filters(self) -> "list[Filter]":
        return self._get_by_agent_type("filter")

    @property
    def watchers(self) -> "list[Watcher]":
        return self._get_by_agent_type("watcher")

    """Starts loggers first, then filters, then watchers"""
    def start_agents(self):
        self._start_agents(self.loggers)
        self._start_agents(self.filters)
        self._start_agents(self.watchers)

    """Starts a list of agents after checking for each of them that they haven't already been started"""
    @staticmethod
    def _start_agents(agents: "list[Agent]"):
        for agent in agents:
            if not agent.is_alive():
                agent.start()
