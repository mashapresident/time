import vlc
import asyncio

async def play_sound(filename):
    """
    Асинхронна функція для відтворення MP3-файлу за допомогою VLC.
    Файл завантажується за допомогою MediaPlayer, а відтворення триває до завершення.
    """
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(filename)
    player.set_media(media)

    player.play()
    await asyncio.sleep(0.2)
    while True:
        state = player.get_state()
        # Якщо відтворення завершилось або виникла помилка – виходимо з циклу
        if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            break
        await asyncio.sleep(0.1)

