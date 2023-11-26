import pyaudio
import numpy as np

# SET PYAUDIO PARAMETERS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024 # number of audio frames to be examined in each chunk
             # this is key to achieving low latency, to find a balance adjust this

# CREATE PYAUDIO INSTANCE
audio = pyaudio.PyAudio()

# OPEN THE STREAM FOR LIVE AUDIO INPUT
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

print("NOW CAPTURING AUDIO...")

try:
    while True:  # keep processing audio chunks forever
        data = stream.read(CHUNK)
        # convert the chunk to numpy array and calculate the volume
        numpydata = np.frombuffer(data, dtype=np.int16)

        # fast fourier transform, converts the time-domain audio signal into its frequency-domain representation.
        fft_result = np.fft.fft(numpydata)
        fft_abs = np.abs(fft_result)

        #
        freqs = np.fft.fftfreq(len(fft_result)) * RATE

        bass_freq_range = (20, 160)  # Define bass frequency range
        threshold = 1000000  # Define a threshold for detecting beats

        for i, freq in enumerate(freqs):
            if bass_freq_range[0] <= freq <= bass_freq_range[1]:
                print(fft_abs[i])
                if fft_abs[i] > threshold:
                    print(f"Bass beat detected at frequency: {freq} Hz")
                    # Add your video switching logic here


        # TODO: Add more sophisticated audio processing here

except KeyboardInterrupt:
    # Stop the stream gracefully, ctrl+c
    print("Finished processing.")

    stream.stop_stream()
    stream.close()
    audio.terminate()
