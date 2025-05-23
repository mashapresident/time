import vlc
from time import *
import asyncio
import time
from load_config import UPLOAD_FOLDER, REGULAR_MUSIC_FOLDER
async def play_melody(filename: str, knock: bool, hour: int):
    """
    Відтворює MP3-файл за допомогою VLC, блокуючи виконання, поки файл не завершиться.
    Якщо `knock=True`, після мелодії запускається відтворення звуку клаку `hour` разів.
    """
    filepath = UPLOAD_FOLDER + "/" + filename
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(filepath)
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
        filepath = REGULAR_MUSIC_FOLDER + "/knock.mp3"
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(filepath)
        player.set_media(media)

        player.play()
        time.sleep(0.2)

        while player.get_state() not in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            time.sleep(0.1)

        await asyncio.sleep(0.5)
