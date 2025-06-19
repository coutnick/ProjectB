import asyncio
from fastapi import FastAPI

from run_bot import run_bot

app = FastAPI()

bot_task: asyncio.Task | None = None

@app.post("/start")
async def start_trading():
    global bot_task
    if bot_task is None or bot_task.done():
        bot_task = asyncio.create_task(run_bot())
        return {"status": "started"}
    return {"status": "already running"}

@app.post("/stop")
async def stop_trading():
    global bot_task
    if bot_task is not None and not bot_task.done():
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass
        return {"status": "stopped"}
    return {"status": "not running"}

@app.get("/status")
async def status():
    running = bot_task is not None and not bot_task.done()
    return {"running": running}
