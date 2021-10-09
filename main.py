from dotenv import load_dotenv

load_dotenv()

from src.control import Control
import src.server as server

control = Control()

if __name__ == "__main__":
    server.doing()
    control.doing()