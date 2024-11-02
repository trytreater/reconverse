## API
class APIConfig:
    """Base configuration with defaults."""
    DEBUG = False

class APIDevelopmentConfig(APIConfig):
    DEBUG = True

class APITestingConfig(APIConfig):
    pass