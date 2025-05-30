import asyncio
import os
from load_config import UPLOAD_FOLDER, REGULAR_MUSIC_FOLDER

async def play_with_mpv(filepath):
    if not os.path.exists(filepath):
        print(f"[ERROR] Файл не знайдено: {filepath}")
        return

    process = await asyncio.create_subprocess_exec(
        "mpv", "--no-terminal", "--quiet", filepath,
        stdout=asyncio.subprocess.DEVNULL,
        stderr=asyncio.subprocess.DEVNULL
    )
    await process.communicate()

async def play_melody(filename: str, knock: bool, hour: int):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    await play_with_mpv(filepath)

    if knock:
        await play_knock(hour)

async def play_knock(hour: int):
    filepath = os.path.join(REGULAR_MUSIC_FOLDER, "knock.mp3")
    for i in range(hour):
        await play_with_mpv(filepath)
        await asyncio.sleep(0.5)
