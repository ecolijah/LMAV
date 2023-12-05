import pyaudio
import numpy as np
import time

# SET PYAUDIO PARAMETERS
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024  # number of audio frames to be examined in each chunk
             # this is key to achieving low latency, to find a balance adjust this

# CREATE PYAUDIO INSTANCE
audio = pyaudio.PyAudio()

# OPEN THE STREAM FOR LIVE AUDIO INPUT
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

bass_hit = False
bass_freq_range = (20, 160)  # Define bass frequency range
threshold = 1000000  # Define a volume threshold for detecting beats

print("NOW CAPTURING AUDIO...")

# continuous while loop
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

        
        if not bass_hit:
            for i, freq in enumerate(freqs):
                if (bass_freq_range[0] <= freq <= bass_freq_range[1] and bass_hit == False): #bass detected
                    # print(fft_abs[i])
                    if fft_abs[i] > threshold :
                        print(f"Bass beat detected at frequency: {freq} Hz")
                        # Add video switching logic here
                        bass_hit = True
                        # threshold = fft_abs[i]
                        print("Threshold: ", threshold)
                        break 
        # time.sleep(1) 

        if bass_hit: 
            for i, freq in enumerate(freqs): 
                if (fft_abs[i] > threshold and bass_freq_range[0] <= freq <= bass_freq_range[1]):
                    print("bass")
                    break
                elif (freq >= bass_freq_range[1]): #check
                    print("bass ended.")
                    bass_hit = False
                    
                    break
        
            
                



except KeyboardInterrupt:
    # Stop the stream gracefully, ctrl+c
    print("Finished processing.")

    stream.stop_stream()
    stream.close()
    audio.terminate()
