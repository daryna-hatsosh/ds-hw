import asyncio
from typing import Dict, Tuple
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')

class MessageHub():
    def __init__(self, start_count = 0):
        self.message_id_counter = start_count
        self.messages = []
    
    def _increase_count(self):
        self.message_id_counter += 1
    
    def add_message(self, message):
        self._increase_count()
        message = {"message_id": self.message_id_counter, "message": message}
        self.messages.append(message)
        return message
    
    def get_messages(self):
        return self.messages
    
    def get_current_message_id_counter(self):
        return self.message_id_counter

def post(server, message):
    try:
        logger.info(f"Making request to {server}")
        response = requests.post(f"http://{server}/messages", params=message)
        logger.info(f"Received response from {server}")
        return {"status_code": response.status_code, "server": server}
    except:
        return {"status_code": -1, "server": server}

async def ping(server, results, message):
    loop = asyncio.get_event_loop()
    future_result = loop.run_in_executor(None, post, server, message)
    result = await future_result
    if result["status_code"] in range(200, 299):
        results["success"].append(server)
    else:
        results["failure"].append(server)

async def make_requests(servers, results, message):
    tasks = []
    for server in servers:
        task = asyncio.create_task(ping(server, results, message))
        tasks.append(task)
    await asyncio.gather(*tasks)

def ping_servers(servers, message: Dict[int, str]):
    results = {"success": [], "failure": []}
    asyncio.run(make_requests(servers, results, message))
    return results
