import vlc
import asyncio
import os
from load_config import UPLOAD_FOLDER, REGULAR_MUSIC_FOLDER

async def play_melody(filename: str, knock: bool, hour: int):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    instance = vlc.Instance()
    if instance is None:
        raise RuntimeError("VLC не ініціалізувався. Перевір, чи встановлено VLC/libvlc.")

    player = instance.media_player_new()
    media = instance.media_new(filepath)
    player.set_media(media)

    player.play()
    await asyncio.sleep(0.2)

    while player.get_state() not in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
        await asyncio.sleep(0.1)

    if knock:
        await play_knock(hour)

async def play_knock(hour: int):
    for i in range(hour):
        filepath = os.path.join(REGULAR_MUSIC_FOLDER, "knock.mp3")
        instance = vlc.Instance()
        player = instance.media_player_new()
        media = instance.media_new(filepath)
        player.set_media(media)

        player.play()
        await asyncio.sleep(0.2)

        while player.get_state() not in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            await asyncio.sleep(0.1)

        await asyncio.sleep(0.5)
