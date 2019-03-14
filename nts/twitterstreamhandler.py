from tweepy import OAuthHandler, Stream
from tweepy.streaming import StreamListener

from nts.confighandler import Config


class TwitterStreamListener(StreamListener):
    def __init__(self, write_method: callable):
        self.filter_list = None
        self.write_method = write_method
        super().__init__()

    def set_filter_list(self, list):
        self.filter_list = list

    def on_data(self, data):
        self.write_method(data, self.filter_list)

    def on_error(self, status):
        print(f'Streaming API error, status code: {status}')


class TwitterStream(Stream):
    def __init__(self, listener: TwitterStreamListener, settings: dict = None):
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

        self.listener = listener
        super().__init__(auth, self.listener)

    def start_filter(self, filter: list, use_async: bool):
        if use_async:
            self.filter(track=filter, is_async=use_async)
        else:
            self.filter(track=filter)
        self.listener.set_filter_list(filter)

    def stop_filter(self):
        self.disconnect()


class TwitterStreamHandler(object):
    def __init__(self, write_method: callable):
        self.twitter_listener = TwitterStreamListener(write_method)
        self.twitter_stream = TwitterStream(self.twitter_listener)

    def start_filter(self, filter: list, use_async: bool):
        self.twitter_stream.start_filter(filter, use_async)

    def stop_filter(self):
        self.twitter_stream.stop_filter()
