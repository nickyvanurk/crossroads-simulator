#!/usr/bin/env python3

import asyncio
import websockets
import json

async def index(websocket, path):
  async for message in websocket:
    data = json.loads(message)

    print(f"< {data}")

    await websocket.send(json.dumps({ 'type': 'pong' }))

start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()