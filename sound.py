import vlc
import asyncio
import time


def play_sound(filename):
    """
    Синхронна функція для відтворення MP3-файлу за допомогою VLC.
    Функція блокує виконання, поки медіа не завершить відтворення.
    """
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(filename)
    player.set_media(media)

    player.play()
    # Дамо плеєру кілька сотих секунди для старту відтворення
    time.sleep(0.2)
    while True:
        state = player.get_state()
        # Якщо відтворення завершилося або виникла помилка – виходимо з циклу
        if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
            break
        time.sleep(0.1)


async def play(hour):
    """
    Асинхронна функція, яка спочатку відтворює мелодію,
    а потім відтворює звук клаку (clock sound) hour разів.
    """
    # Спочатку відтворюємо мелодію (фіксована назва файлу)
    play_sound( "music/melodiya_audio.mp3")

    # Потім відтворюємо звук клаку hour разів (рахунок починається з 1)
    for i in range(1, hour + 1):
        print(f"Відтворення звуку клаку — ітерація {i}")
        play_sound("music/stuk_audio.mp3")

