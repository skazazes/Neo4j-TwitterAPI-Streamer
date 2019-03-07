from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener
import json

from confighandler import Config


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


class TwitterStreamListener(StreamListener):
    def on_data(self, data):
        pass

    def on_error(self, status):
        print(f'Streaming API error, status code: {status}')


class TwitterStreamHandler(object):
    def __init__(self):
        self.twitter_stream = TwitterStream()
        self.twitter_stream_listener = TwitterStreamListener()

    def set_write_tweet_method(self, method: callable):
        self.twitter_stream_listener.on_data = method
