from tweepy import OAuthHandler, Stream
from twitterstremlistener import TwitterStreamListener


class TwitterStream(Stream):
    def __init__(self, config):
        auth = OAuthHandler(config.TWITTER_API_KEY,
                            config.TWITTER_API_SECRET)
        auth.set_access_token(config.TWITTER_ACCESS_TOKEN,
                              config.TWITTER_ACCESS_TOKEN_SECRET)
        listener = TwitterStreamListener(config)
        super().__init__(auth, listener)

    def start_filter(self, filter: list, use_async: bool):
        if use_async:
            self.filter(track=filter, is_async=use_async)
        else:
            self.filter(track=filter)
