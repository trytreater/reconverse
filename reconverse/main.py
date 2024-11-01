from dotenv import load_dotenv
from .reconverse import Reconverse
from . import create_api

def main(env: str):
    print("Booting up Reconverse...")
    print("Environment:", env)
    load_dotenv(f".env.{env}")

    server = Reconverse(env)

    api = create_api(server, env)

    if env == "development" or env == "testing":
        debug=True
    else:
        debug=False

    api.run(host='127.0.0.1', port=5000, debug=debug)



    server.logger.info("Successfully booted up Reconverse.")

