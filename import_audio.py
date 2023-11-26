import pyaudio
import numpy as np

# SET PYAUDIO PARAMETERS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# CREATE PYAUDIO INSTANCE
audio = pyaudio.PyAudio()

# OPEN THE STREAM FOR LIVE AUDIO INPUT
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("NOW CAPTURING AUDIO...")

try:
    while True:  # Keep processing audio chunks forever
        data = stream.read(CHUNK)
        # Convert the chunk to numpy array and calculate the volume
        numpydata = np.frombuffer(data, dtype=np.int16)
        volume = np.linalg.norm(numpydata) * 10
        print(f"Volume: {volume}")

        # TODO: Add more sophisticated audio processing here

except KeyboardInterrupt:
    # Stop the stream gracefully
    print("Finished processing.")

    stream.stop_stream()
    stream.close()
    audio.terminate()
