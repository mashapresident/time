import vlc
from time import *
import asyncio
import time
from load_config import UPLOAD_FOLDER
def play_melody(filename: str, knock: bool, hour: int):
    """
    Відтворює MP3-файл за допомогою VLC, блокуючи виконання, поки файл не завершиться.
    Якщо `knock=True`, після мелодії запускається відтворення звуку клаку `hour` разів.
    """
    filepath = UPLOAD_FOLDER + filename
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(filename)
    player.set_media(media)

    player.play()
    time.sleep(0.2)

    while player.get_state() not in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
        time.sleep(0.1)

    if knock:
        asyncio.run(play_knock(hour))


async def play_knock(hour: int):
    """
    Асинхронно відтворює звук клаку `hour` разів із паузою між кожним ударом.
    """
    for i in range(hour):
        print(f"Відтворення звуку клаку — {i + 1}-й удар")
        await asyncio.sleep(0.5)
