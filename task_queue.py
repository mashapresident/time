import asyncio
import inspect

global_queue = asyncio.Queue()
global_mutex = asyncio.Lock()

async def enqueue_task(func, *args, **kwargs):
    """Додає завдання до асинхронної черги."""
    await global_queue.put((func, args, kwargs))

async def process_queue():
    """Фоново обробляє завдання по черзі."""
    while True:
        func, args, kwargs = await global_queue.get()
        try:
            async with global_mutex:
                if inspect.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    await asyncio.to_thread(func, *args, **kwargs)
        except Exception as e:
            print(f"[ERROR] Помилка виконання завдання: {e}")
        finally:
            global_queue.task_done()