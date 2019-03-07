import configparser


class Config(object):
    # Create config parser object
    config = configparser.ConfigParser()

    # Attempt to open provided config file
    try:
        with open('../config.ini', 'r') as f:
            config.read_file(f)
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
    TWITTER_API_KEY = (
        config['Twitter API Settings']['API_KEY']
        )
    TWITTER_API_SECRET = (
        config['Twitter API Settings']['API_SECRET']
        )
    TWITTER_ACCESS_TOKEN = (
        config['Twitter API Settings']['ACCESS_TOKEN']
        )
    TWITTER_ACCESS_TOKEN_SECRET = (
        config['Twitter API Settings']['ACCESS_TOKEN_SECRET']
        )

    NEO4J_HOST = (
        config['Neo4J Settings']['NEO4J_HOST']
        )
    NEO4J_USER = (
        config['Neo4J Settings']['NEO4J_USER']
        )
    NEO4J_PASSWORD = (
        config['Neo4J Settings']['NEO4J_PASSWORD']
        )

    def set_settings(settings: dict):
        for key in settings:
            setattr(Config, key, settings[key])

    def set_twitter_api_key(key: str):
        Config.TWITTER_API_KEY = key

    def set_twitter_api_secret(secret: str):
        Config.TWITTER_API_SECRET = secret

    def set_twitter_access_token(token: str):
        Config.TWITTER_ACCESS_TOKEN = token

    def set_twitter_access_token_secret(secret: str):
        Config.TWITTER_ACCESS_TOKEN_SECRET = secret

    def set_neo4j_host(host: str):
        Config.NEO4J_HOST = host

    def set_neo4j_user(user: str):
        Config.NEO4J_USER = user

    def set_neo4j_password(password: str):
        Config.NEO4J_PASSWORD = password
