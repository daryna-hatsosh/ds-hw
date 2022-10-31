import logging
import random
import time

from common.http_servers import HealthStatus
from fastapi import FastAPI
from fastapi import HTTPException

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

message_list = []
logger.info("INFO: secondary booted up")


@app.get("/messages")
def read_root():
    return message_list


@app.get("/health")
def read_root():
    return {"status": HealthStatus.healthy}


@app.post("/messages")
def create_message(message_id: int, message: str):
    logger.info("Before sleep")
    wait_time = random.randint(5, 10)
    time.sleep(wait_time)
    logger.info(f"After sleep for {wait_time} seconds")
    logger.info("Last message_id:")
    last_in_list = 0
    messages_ids = []
    if message_list:
        last_in_list = message_list[-1]["message_id"]
        logger.info(last_in_list)
        messages_ids = [mess["message_id"] for mess in message_list]

    if _check_if_order_is_correct(last_in_list, message_id):
        missing_ids = _find_missing(messages_ids)
        if missing_ids:
            logger.info("Missing ids: ", missing_ids)
            raise HTTPException(status_code=500, detail="Message could not be added.")
        else:
            message_list.append({"message_id": message_id, "message": message})
            logger.info("Created message on secondary")
    else:
        raise HTTPException(status_code=500, detail="Message could not be added.")
    return message_list


def _find_missing(lst):
    if not lst:
        return []
    return sorted(set(range(lst[0], lst[-1])) - set(lst))


def _check_if_order_is_correct(last_in_list, next_id):
    return next_id - last_in_list == 1
