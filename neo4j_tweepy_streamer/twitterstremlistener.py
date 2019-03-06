from tweepy.streaming import StreamListener

import json


class TwitterStreamListener(StreamListener):
    def __init__(self, config):
        self.config = config

    def on_data(self, data):
        json_data = json.loads(data)
        print(json_data)
        return True

    def on_error(self, status):
        print(f'Streaming API error, status code: {status}')
