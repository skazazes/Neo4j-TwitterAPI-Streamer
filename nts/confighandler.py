class Config(object):
    TWITTER_API_KEY = ''
    TWITTER_API_SECRET = ''
    TWITTER_ACCESS_TOKEN = ''
    TWITTER_ACCESS_TOKEN_SECRET = ''

    NEO4J_HOST = ''
    NEO4J_PORT = ''
    NEO4J_USER = ''
    NEO4J_SCHEME = ''
    NEO4J_PASSWORD = ''

    def __init__(self, settings: dict):
        self.set_settings(settings)

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

    def set_neo4j_scheme(scheme: str):
        Config.NEO4J_SCHEME = scheme

    def set_neo4j_port(port: int):
        Config.NEO4J_PORT = port
