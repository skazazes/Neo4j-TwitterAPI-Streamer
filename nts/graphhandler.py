from py2neo import Graph, Node, Relationship
from copy import deepcopy
import json

from nts.confighandler import Config


class Deserializer(object):
    def create_hashtag_node(self, hashtag) -> Node:
        hashtag_node = Node('Hashtag', tag=hashtag['text'])
        hashtag_node.__primarykey__ = 'tag'
        hashtag_node.__primarylabel__ = 'Hashtag'
        return hashtag_node

    def create_URL_node(self, url) -> Node:
        url_node = Node('URL',
                        url=url['url'],
                        expanded_url=url['expanded_url'],
                        display_url=url['display_url'])
        url_node.__primarykey__ = 'url'
        url_node.__primarylabel__ = 'URL'

        return url_node

    def create_source_node(self, source) -> Node:
        source_node = Node('Source', type=source)
        source_node.__primarykey__ = 'type'
        source_node.__primarylabel__ = 'Source'
        return source_node

    def create_user_node(self, user) -> Node:
        user_node = Node('User', **user)
        user_node.__primarykey__ = 'id'
        user_node.__primarylabel__ = 'User'
        return user_node

    def create_tweet_node(self, tweet) -> Node:
        tweet_node = Node('Tweet', **tweet)
        tweet_node.__primarykey__ = 'id'
        tweet_node.__primarylabel__ = 'Tweet'
        return tweet_node

    def deserialize_tweet(self, origonal_tweet) -> dict:
        tweet = deepcopy(origonal_tweet)

        # Remove unneeded dicts from tweet dict (duplicate or unused data)
        # Extract needed dicts from tweet dict, reassign tweet to tweet_data
        retweeted_status = None
        retweeted_status_user = None
        quoted_status = None

        if 'retweeted_status' in tweet:
            retweeted_status_dict = tweet.pop('retweeted_status')
            retweeted_status_user = (
                    self.create_user_node(
                            {'id': retweeted_status_dict['user']['id']}
                        )
                )
            retweeted_status = (
                    self.create_tweet_node(
                            {'id': retweeted_status_dict['id']}
                        )
                )
        if 'quoted_status' in tweet:
            quoted_status_dict = tweet.pop('quoted_status')
            quoted_status = (
                    self.create_tweet_node(
                        {'id': quoted_status_dict['id']}
                    )
                )
            del tweet['quoted_status_permalink']
        if 'extended_entities' in tweet:
            del tweet['extended_entities']
        if 'place' in tweet:
            del tweet['place']

        user_data = tweet.pop('user')
        entities_data = tweet.pop('entities', None)
        extended_data = tweet.pop('extended_tweet', None)

        # If extended_data exists, merge extended data in proper locations
        if extended_data:
            tweet['text'] = extended_data['full_text']
            entities_data = extended_data['entities']

        # Create nodes for hashtags, urls, source, and user mentions
        hashtag_nodes = []
        for hashtag in entities_data['hashtags']:
            hashtag_nodes.append(self.create_hashtag_node(hashtag))

        url_nodes = []
        for url in entities_data['urls']:
            url_nodes.append(self.create_URL_node(url))

        user_mention_nodes = []
        for user_mention in entities_data['user_mentions']:
            del user_mention['indices']
            user_mention_nodes.append(self.create_user_node(user_mention))

        cut_source = tweet.pop('source').split('>')[1].split('<')[0]
        source_node = self.create_source_node(cut_source)

        # Create user and tweet nodes from dictionaries
        user_node = self.create_user_node(user_data)
        tweet_node = self.create_tweet_node(tweet)

        # Prep final nodes dict
        nodes_dict = {
            'hashtag_nodes': hashtag_nodes,
            'url_nodes': url_nodes,
            'source_node': source_node,
            'user_mention_nodes': user_mention_nodes,
            'user_node': user_node,
            'tweet_node': tweet_node,
            'quoted_status': quoted_status,
            'retweeted_status': retweeted_status,
            'retweeted_status_user': retweeted_status_user
        }

        return nodes_dict


class Relationships(object):
    HAS_TAG = Relationship.type('HAS_TAG')
    HAS_LINK = Relationship.type('HAS_LINK')
    POSTED_VIA = Relationship.type('POSTED_VIA')
    POSTED = Relationship.type('POSTED')
    MENTIONS = Relationship.type('MENTIONS')
    RETWEETS = Relationship.type('RETWEETS')


class GraphHandler(object):
    deserializer = Deserializer()
    relationships = Relationships()

    def __init__(self, settings: dict = None):
        if settings:
            self.graph = Graph(scheme=settings['NEO4J_SCHEME'],
                               port=settings['NEO4J_PORT'],
                               host=settings['NEO4J_HOST'],
                               auth=(settings['NEO4J_USER'],
                                     settings['NEO4J_PASSWORD']))
        else:
            self.graph = Graph(scheme=Config.NEO4J_SCHEME,
                               port=Config.NEO4J_PORT,
                               host=Config.NEO4J_HOST,
                               auth=(Config.NEO4J_USER,
                                     Config.NEO4J_PASSWORD))

    def on_data(self, extra, tweet):
        self.write_tweet_and_subtweets(json.loads(tweet))
        return True

    def write_tweet_and_subtweets(self,
                                  tweet,
                                  check_retweet: bool = True,
                                  check_quote_tweet: bool = False):
        # Go to deepest tweet, recall on self if current tweet is deepest
        if check_retweet:
            if 'retweeted_status' in tweet:
                self.write_tweet_and_subtweets(tweet['retweeted_status'],
                                               True, True)
                self.write_tweet_and_subtweets(tweet, False, True)
            else:
                self.write_tweet_and_subtweets(tweet, False, True)
        elif check_quote_tweet:
            if 'quoted_status' in tweet:
                self.write_tweet_and_subtweets(tweet['quoted_status'],
                                               True, False)
                self.write_tweet_and_subtweets(tweet, False, False)
            else:
                self.write_tweet_and_subtweets(tweet, False, False)
        else:
            self.write_tweet(tweet)

    def write_tweet(self, tweet: dict):
        tweet_nodes = GraphHandler.deserializer.deserialize_tweet(tweet)

        # User POSTED Tweet
        self.graph.merge(
            GraphHandler.relationships.POSTED(
                tweet_nodes['user_node'], tweet_nodes['tweet_node']
                ))

        # Tweet POSTED_VIA Source
        self.graph.merge(
            GraphHandler.relationships.POSTED_VIA(
                tweet_nodes['tweet_node'], tweet_nodes['source_node']
            )
        )

        # Tweet HAS_LINK URL
        for url_node in tweet_nodes['url_nodes']:
            self.graph.merge(
                GraphHandler.relationships.HAS_LINK(
                    tweet_nodes['tweet_node'], url_node
                )
            )

        # Tweet HAS_TAG Hashtag
        for hashtag_node in tweet_nodes['hashtag_nodes']:
            self.graph.merge(
                GraphHandler.relationships.HAS_TAG(
                    tweet_nodes['tweet_node'], hashtag_node
                )
            )

        # Tweet MENTIONS User
        for user_node in tweet_nodes['user_mention_nodes']:
            self.graph.merge(
                GraphHandler.relationships.MENTIONS(
                    tweet_nodes['tweet_node'], user_node
                )
            )

        # Tweet MENTIONS Tweet
        if tweet_nodes['quoted_status']:
            self.graph.merge(
                GraphHandler.relationships.MENTIONS(
                    tweet_nodes['tweet_node'], tweet_nodes['quoted_status']
                )
            )

        # Tweet RETWEETS Tweet
        if tweet_nodes['retweeted_status']:
            self.graph.merge(
                GraphHandler.relationships.RETWEETS(
                    tweet_nodes['tweet_node'], tweet_nodes['retweeted_status']
                )
            )

            self.graph.merge(
                GraphHandler.relationships.RETWEETS(
                    tweet_nodes['user_node'],
                    tweet_nodes['retweeted_status_user']
                )
            )
