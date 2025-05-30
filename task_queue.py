# task_queue.py
import asyncio
import inspect

global_queue = asyncio.Queue()
global_mutex = asyncio.Lock()

async def enqueue_task(func, *args, **kwargs):
    await global_queue.put((func, args, kwargs))

async def process_queue():
    while True:
        func, args, kwargs = await global_queue.get()
        try:
            async with global_mutex:
                if inspect.iscoroutinefunction(func):
                    await func(*args, **kwargs)
                else:
                    await asyncio.to_thread(func, *args, **kwargs)
        except Exception as e:
            print(f"[ERROR] Queue task failed: {e}")
        finally:
            global_queue.task_done()
