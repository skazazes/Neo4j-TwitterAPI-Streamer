from twitterstreamhandler import TwitterStreamHandler, TwitterStreamListener
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

        TwitterStreamListener.addMethod(self.graph_handler.on_data)

    def start_filter(self, filter: list, use_async: bool = False):
        self.twitter_stream_handler.start_filter(filter, use_async)


sw = StreamWriter()

# Not yet working, not sure why but its 2AM
sw.start_filter(['eth', 'ethereum', 'btc', 'bitcoin'])
