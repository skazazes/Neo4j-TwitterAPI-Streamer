from twitterstreamhandler import TwitterStreamHandler
from graphhandler import GraphHandler


class StreamWriter(object):
    def __init__(self, settings: dict = None):
        if settings:
            self.twitter_stream_handler = TwitterStreamHandler(
                settings=settings)
            self.graph_handler = GraphHandler(settings=settings)
        else:
            self.twitter_stream_handler = TwitterStreamHandler()
            self.graph_handler = GraphHandler()
