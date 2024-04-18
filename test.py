import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

p = pyaudio.PyAudio()


for index in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(index)
    print(f"Device {index}: {device_info['name']}")


input_device_index = p.get_default_input_device_info()['index']


input_channels = p.get_device_info_by_index(input_device_index)['maxInputChannels']

stream = p.open(format=FORMAT,
                channels=input_channels,
                rate=RATE,
                input=True,
                input_device_index=input_device_index,
                frames_per_buffer=CHUNK)

print("* Recording audio...")

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("* Finished recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(input_channels)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
