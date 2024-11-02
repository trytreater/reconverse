from dotenv import load_dotenv
from reconverse.server.reconverse import Reconverse


def main(env: str):
    print("Booting up Reconverse...")
    print("Environment:", env)
    load_dotenv(f".env.{env}")

    server = Reconverse(env)

    server.logger.info("Successfully booted up Reconverse.")
