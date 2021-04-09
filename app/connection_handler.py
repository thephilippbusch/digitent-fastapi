from fastapi import WebSocket
from typing import List 

class ConnectionHandler:
    def __init__(self):
        self.connections: List[dict] = []

    async def connect(self, ws: WebSocket, channel: str):
        await ws.accept()
        self.connections.append({
            "socket": ws,
            "channel": channel
        })

    async def broadcast(self, message: dict):
        for connection in self.connections:
            await connection["socket"].send_json(message)

    async def send_to_room(self, message: dict, channel: str):
        for connection in self.connections:
            if connection["channel"] == channel:
                await connection["socket"].send_json(message)