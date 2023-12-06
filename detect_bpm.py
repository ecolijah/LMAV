import pyaudio
import numpy as np
import time
import librosa
import librosa.display

# Constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
AUDIO_DEVICE_INDEX = 0  # Change based on your audio device
N_FFT = 256     # This parameter specifies the length of the Fast Fourier Transform (FFT) window, 
                # which determines the time-frequency resolution of the analysis. 

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open stream
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

def process_audio(data):
    # Convert data to numpy array and normalize to range [-1, 1]
    audio_data = np.frombuffer(data, dtype=np.int16) / 32768.0

    # Calculate onset envelope
    onset_env = librosa.onset.onset_strength(y=audio_data, sr=RATE, n_fft=N_FFT)

    # Estimate tempo (BPM) from the onset envelope
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=RATE)

    return tempo

def metronome(bpm):
    if bpm == 0:
        bpm = 60
    beat_interval = 60 / bpm
    next_beat_time = time.time() + beat_interval
    c = 1
    while True:
        current_time = time.time()
        if current_time >= next_beat_time:
            
            print(c)
            c += 1
            next_beat_time += beat_interval

def main():
    print("Starting audio processing...")
    try:
        while True:
            data = stream.read(CHUNK)
            bpm = process_audio(data)
            print(bpm)
            metronome(bpm)
    except KeyboardInterrupt:
        print("\nStopping...")
        print("BPM: ", bpm)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()

if __name__ == "__main__":
    main()
