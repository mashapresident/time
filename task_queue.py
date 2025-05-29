from multiprocessing import Process, Lock
import queue
import asyncio
global_queue = queue.Queue()
global_mutex = asyncio.Lock()  # Додаємо м'ютекс


def enqueue_task(func, *args, **kwargs):
    """Додає функцію до черги."""
    global_queue.put((func, args, kwargs))


async def process_queue():
    """Обробляє завдання з черги в порядку їх надходження."""
    while True:
        try:
            func, args, kwargs = global_queue.get_nowait()
            async with global_mutex:  # Використання асинхронного блокування
                await asyncio.to_thread(func, *args, **kwargs)
        except queue.Empty:
            await asyncio.sleep(0.1)