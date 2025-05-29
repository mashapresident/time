from multiprocessing import Process, Lock
import queue
import asyncio
global_queue = queue.Queue()
global_mutex = Lock()  # Додаємо м'ютекс


def enqueue_task(func, *args, **kwargs):
    """Додає функцію до черги."""
    global_queue.put((func, args, kwargs))


async def process_queue():
    """Обробляє завдання з черги в порядку їх надходження."""
    while True:
        func, args, kwargs = global_queue.get()
        with global_mutex:  # Захист спільних ресурсів
            await asyncio.to_thread(func, *args, **kwargs)