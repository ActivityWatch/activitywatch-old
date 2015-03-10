import json

from flask import Flask, make_response
import logging

from activitywatch.modulemanager import ModuleManager
from activitywatch.base import Logger

app = Flask(__name__, static_url_path='', static_folder='../site')


def agent_to_json(agent) -> dict:
    return {"name": agent.identifier,
            "type": agent.agent_type,
            "alive": agent.is_alive(),
            "threadId": agent.ident}

"""
One page app handler, always returns index.html
For some strange reason @app.route("/<path:_>") didn't work,
this should be investigated but for now the below works
"""
@app.route("/")
@app.route("/<_>")
@app.route("/<_>/<__>")
@app.route("/<_>/<__>/<___>")
def index(**_):
    return app.send_static_file("index.html")


@app.route("/api/0/agents")
def get_agents():
    agents = []
    for agent in ModuleManager().agents:
        agents.append(agent_to_json(agent))
    return json.dumps(agents)


@app.route("/api/0/agents/<int:agent_id>")
def get_agent(agent_id):
    for agent in ModuleManager().agents:
        if agent._ident == agent_id:
            return json.dumps(agent_to_json(agent))
    return make_response("Resource not found", 400)


@app.route("/scripts/<file>")
def scripts(file):
    return app.send_static_file("scripts/" + file)


@app.route("/templates/<file>")
def templates(file):
    return app.send_static_file("templates/" + file)


class RestLogger(Logger):
    def run(self):
        app.run()

if __name__ == "__main__":
    RestLogger().start()