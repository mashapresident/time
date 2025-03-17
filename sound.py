import alsaaudio
import wave


async def play(filename):
    # Відкриття WAV-файлу
    wav = wave.open(filename, 'rb')

    # Налаштування аудіовиходу
    output = alsaaudio.PCM(alsaaudio.PCM_PLAYBACK, device='hw:1,0')
    output.setchannels(wav.getnchannels())
    output.setrate(wav.getframerate())
    output.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    output.setperiodsize(1024)

    # Відтворення аудіо
    data = wav.readframes(1024)
    while data:
        output.write(data)
        data = wav.readframes(1024)

    wav.close()

