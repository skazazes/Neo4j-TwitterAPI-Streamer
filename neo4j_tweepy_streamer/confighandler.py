import configparser


class Config(object):
    def __init__(self):
        # Create config parser object
        self.config = configparser.ConfigParser()

        # Attempt to open provided config file
        try:
            with open('../config.ini', 'r') as f:
                self.config.read_file(f)
        except FileNotFoundError:
            print('Config Error: Config file not found!')
            exit()
        except configparser.MissingSectionHeaderError:
            print(('Config Error: Config missing section header!)'))
            exit()
        except configparser.ParsingError:
            print('Config Error: Config parsing error!')
            exit()

        # Assign neccisary variables
        self.TWITTER_API_KEY = (
            self.config['Twitter API Settings']['API_KEY']
            )
        self.TWITTER_API_SECRET = (
            self.config['Twitter API Settings']['API_SECRET']
            )
        self.TWITTER_ACCESS_TOKEN = (
            self.config['Twitter API Settings']['ACCESS_TOKEN']
            )
        self.TWITTER_ACCESS_TOKEN_SECRET = (
            self.config['Twitter API Settings']['ACCESS_TOKEN_SECRET']
            )

        self.NEO4J_HOST = (
            self.config['Neo4J Settings']['NEO4J_HOST']
            )
        self.NEO4J_USER = (
            self.config['Neo4J Settings']['NEO4J_USER']
            )
        self.NEO4J_PASSWORD = (
            self.config['Neo4J Settings']['NEO4J_PASSWORD']
            )
