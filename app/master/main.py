import logging

import uvicorn
from common.http_servers import MessageHub
from common.http_servers import ping_servers
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    sec_url_1: str = "test_1"
    sec_url_2: str = "test"

    class Config:
        env_file = ".env"


settings = Settings()
message_hub = MessageHub()

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

logger.info("master booted up")


@app.get("/messages")
def get_messages():
    return message_hub.get_messages()


@app.post("/messages")
def create_message(message: str):
    message_with_id = message_hub.add_message(message)
    logger.info("PING SERVERS")
    logger.info(message_with_id)
    results = ping_servers([settings.sec_url_1, settings.sec_url_2], message_with_id)
    logger.info(results)
    return results


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5050)
