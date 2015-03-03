import json

from flask import Flask, make_response
import logging

from activitywatch.modulemanager import ModuleManager
from activitywatch.base import Logger

app = Flask(__name__, static_url_path='', static_folder='site')


def agent_to_json(agent):
    return {"name": agent.NAME,
            "type": agent.get_agent_type(),
            "alive": agent.is_alive(),
            "id": agent._ident}

@app.route("/api/0/agents")
def get_agents():
    agents = []
    for agent in ModuleManager().get_agents():
        agents.append(agent_to_json(agent))
    return json.dumps(agents)

@app.route("/api/0/agents/<int:agent_id>")
def get_agent(agent_id):
    for agent in ModuleManager().get_agents():
        if agent._ident == agent_id:
            return json.dumps(agent_to_json(agent))
    return make_response("Resource not found", 400)

@app.route("/scripts/<file>")
def scripts(file):
    return app.send_static_file("scripts/" + file)

@app.route("/templates/<file>")
def templates(file):
    return app.send_static_file("templates/" + file)

@app.route("/")
@app.route("/agent/<int:id>")
def index(**_):
    return app.send_static_file("index.html")


class RestLogger(Logger):
    NAME = "rest"

    def run(self):
        app.run()

if __name__ == "__main__":
    RestLogger().start()