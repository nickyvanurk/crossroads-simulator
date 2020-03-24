#!/usr/bin/env python3

import asyncio
import websockets

async def index(websocket, path):
  data = await websocket.recv()
  print(f"< {data}")

  await websocket.send('pong')

start_server = websockets.serve(index, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()