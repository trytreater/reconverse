from flask import Flask
from reconverse.server.routes import configure_routes

class APIConfig:
    """Base configuration with defaults."""
    DEBUG = False

class APIDevelopmentConfig(APIConfig):
    DEBUG = True

class APITestingConfig(APIConfig):
    pass

def create_api(server, env):
    api = Flask(__name__)
    match env:
        case 'development':
            api.config.from_object(APIDevelopmentConfig)
        case 'testing':
            api.config.from_object(APITestingConfig)
        case _:
            raise Exception(f"Invalid environment: {env}")

    configure_routes(server, api)

    return api


