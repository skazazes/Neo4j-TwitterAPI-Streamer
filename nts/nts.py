from twitterstreamhandler import TwitterStreamHandler, TwitterStreamListener
from graphhandler import GraphHandler

from threading import Timer


class Neo4jTwitterStreamer(object):
    def __init__(self, settings: dict = None):
        if settings:
            self.twitter_stream_handler = TwitterStreamHandler(
                settings=settings)
            self.graph_handler = GraphHandler(settings=settings)
        else:
            self.twitter_stream_handler = TwitterStreamHandler()
            self.graph_handler = GraphHandler()

        self.filter_list = []
        self.running = False
        self.timed = False
        self.timer = ''
        TwitterStreamListener.addMethod(self.graph_handler.on_data)

    def add_filter(self, filter):
        if type(filter) == str:
            self.filter_list.append(filter)
        elif type(filter) == list:
            self.filter_list = self.filter_list + filter

    def start_async_stream(self):
        if not self.running:
            self.running = True
            self.twitter_stream_handler.start_filter(self.filter, True)
        else:
            print('Stream already running')

    def stop_async_stream(self):
        if self.running:
            self.twitter_stream_handler.stop_filter()
            self.running = False
            if self.timed:
                self.timer.cancel()
                self.timed = False
        else:
            print('Not streaming')

    def start_async_stream_timed(self, time: int):
        if not self.running:
            self.start_async_stream()
            self.timed = True
            t = Timer(time, self.stop_async_stream)
            t.start()
        else:
            print('Stream already running')

    def start_blocking_stream(self):
        self.running = True
        self.twitter_stream_handler.start_filter(self.filter, False)


# Example
# sw = Neo4jTwitterStreamer()
# sw.start_filter(['eth', 'ethereum', 'btc', 'bitcoin'])
