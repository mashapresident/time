from multiprocessing import Process, Lock
import inspect
import queue
import asyncio
from asyncio import QueueEmpty
global_queue = asyncio.Queue()
global_mutex = asyncio.Lock()  # Додаємо м'ютекс


async def enqueue_task(func, *args, **kwargs):
    """Додає функцію до черги."""
    await global_queue.put((func, args, kwargs))


async def process_queue():
    while True:
        func, args, kwargs = await global_queue.get()
        async with global_mutex:
            if inspect.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                await asyncio.to_thread(func, *args, **kwargs)
        global_queue.task_done()