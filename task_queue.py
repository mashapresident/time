from multiprocessing import Process, Lock
import inspect
import queue
import asyncio
from asyncio import QueueEmpty
global_queue = queue.Queue()
global_mutex = asyncio.Lock()  # Додаємо м'ютекс


async def enqueue_task(func, *args, **kwargs):
    """Додає функцію до черги."""
    await global_queue.put((func, args, kwargs))


async def process_queue():
    """Обробляє завдання з черги в порядку їх надходження."""
    while True:
        try:
            func, args, kwargs = global_queue.get_nowait()

            async with global_mutex:
                if inspect.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    await asyncio.to_thread(func, *args, **kwargs)

        except QueueEmpty:
            await asyncio.sleep(0.1)