from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from confighandler import Config

import types


class TwitterStream(Stream):
    def __init__(self, settings: dict = None):
        if settings:
            auth = OAuthHandler(settings['TWITTER_API_KEY'],
                                settings['TWITTER_API_SECRET'])
            auth.set_access_token(settings['TWITTER_ACCESS_TOKEN'],
                                  settings['TWITTER_ACCESS_TOKEN_SECRET'])
        else:
            auth = OAuthHandler(Config.TWITTER_API_KEY,
                                Config.TWITTER_API_SECRET)
            auth.set_access_token(Config.TWITTER_ACCESS_TOKEN,
                                  Config.TWITTER_ACCESS_TOKEN_SECRET)

        listener = TwitterStreamListener()
        super().__init__(auth, listener)

    def start_filter(self, filter: list, use_async: bool):
        if use_async:
            self.filter(track=filter, is_async=use_async)
        else:
            self.filter(track=filter)

    def stop_filter(self):
        self.disconnect()


class TwitterStreamListener(StreamListener):
    @classmethod
    def addMethod(cls, func):
        return setattr(cls, func.__name__, types.MethodType(func, cls))

    def on_error(self, status):
        print(f'Streaming API error, status code: {status}')


class TwitterStreamHandler(object):
    def __init__(self):
        self.twitter_stream = TwitterStream()
        self.twitter_stream_listener = TwitterStreamListener()

    def start_filter(self, filter: list, use_async: bool):
        self.twitter_stream.start_filter(filter, use_async)
