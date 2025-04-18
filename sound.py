from time import sleep

#import vlc
import asyncio
import time


def play_sound(filename):
    """
    Синхронна функція для відтворення MP3-файлу за допомогою VLC.
    Функція блокує виконання, поки медіа не завершить відтворення.
    """
    #instance = vlc.Instance()
    #player = instance.media_player_new()
    #media = instance.media_new(filename)
    #player.set_media(media)

    #player.play()
    # Дамо плеєру кілька сотих секунди для старту відтворення
    # time.sleep(0.2)
    # while True:
    #     #state = player.get_state()
    #    # if state in (vlc.State.Ended, vlc.State.Stopped, vlc.State.Error):
    #    #     break
    #     time.sleep(0.1)
    print("Грає звук із файлу " + filename)


async def play(hour):
    try:
        await asyncio.to_thread(play_sound, clock.get_melody())
        for i in range(1, hour + 1):
            print(f"Відтворення звуку клаку — ітерація {i}")
            await asyncio.to_thread(play_sound, "music/files/stuk_audio.wav")
            await asyncio.sleep(0.2)
    except Exception as e:
        print(f"An error occurred: {e}")


# Приклад використання:
if __name__ == '__main__':
    # Наприклад, потрібно відтворити звук клаку 3 рази після мелодії
    asyncio.run(play(3))
