#!/usr/bin/env python

import asyncio
import websockets
import json

async def index():
  uri = 'ws://localhost:8765'

  async with websockets.connect(uri) as websocket:
    await websocket.send(json.dumps({ 'type': 'ping' }))

    async for message in websocket:
      print(f"< {message}")

asyncio.get_event_loop().run_until_complete(index())