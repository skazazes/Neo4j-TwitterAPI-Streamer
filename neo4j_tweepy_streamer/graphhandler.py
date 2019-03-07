from py2neo import database
from confighandler import Config


class GraphHandler(object):
    def __init__(self, settings: dict = None):
        if settings:
            self.graph = database.Graph(host=settings['NEO4J_HOST'],
                                        auth=(settings['NEO4J_USER'],
                                              settings['NEO4J_PASSWORD']))
        else:
            self.graph = database.Graph(host=Config.NEO4J_HOST,
                                        auth=(Config.NEO4J_USER,
                                              Config.NEO4J_PASSWORD))
