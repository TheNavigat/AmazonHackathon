import pyaudio
import wave
import boto3

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 22050
CHUNK = 1024
def recordAnswer(WAVE_OUTPUT_FILENAME,RECORD_SECONDS):
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    s3 = boto3.resource('s3')
    s3.Object('testquestions-8853-5742-7832',WAVE_OUTPUT_FILENAME).put(Body=open(WAVE_OUTPUT_FILENAME, 'rb'))

recordAnswer("batee5.wav",10)
