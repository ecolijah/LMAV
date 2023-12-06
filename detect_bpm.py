import pyaudio
import numpy as np
import time
import librosa
import librosa.display
import multiprocessing

# Constants
RECORD_SECONDS = 10
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = RECORD_SECONDS * RATE
AUDIO_DEVICE_INDEX = 0  # Change based on your audio device
N_FFT = 256     # This parameter specifies the length of the Fast Fourier Transform (FFT) window, 
                # which determines the time-frequency resolution of the analysis. 



def process_audio(data):
    # Convert data to numpy array and normalize to range [-1, 1]
    audio_data = np.frombuffer(data, dtype=np.int16) / 32768.0

    # Calculate onset envelope
    onset_env = librosa.onset.onset_strength(y=audio_data, sr=RATE, n_fft=N_FFT)

    # Estimate tempo (BPM) from the onset envelope
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=RATE)

    return tempo

def metronome(bpm):
    
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

        # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # sampleRate = int(default_speakers['defaultSampleRate'])
    # chunk = sampleRate * RECORD_SECONDS

    # Open stream
    

    
    #CALL METRONOME FUNCTION on repeat
    try: 
        while True:
            #open audio stream
            stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
            print(f"Recording {RECORD_SECONDS} seconds.")

            #read the desired chunk size
            sound = stream.read(CHUNK)
            print("Recording complete 🎹")

            #close stream
            stream.stop_stream()
            stream.close()
            print("Analyzing BPM 🎵")

            #load sounda data into numpy array
            np_sound = np.frombuffer(sound, dtype=np.int16)  / 32768.0 #normalize levels

            #call beat detection librosa method
            tempo, beat_frames = librosa.beat.beat_track(y=np_sound, sr=RATE)

            if tempo < 90:
                print(f'Estimated tempo: {(tempo)} or {(tempo * 2)} bpm')
            else:
                print(f'Estimated tempo: {(tempo)} bpm')
            
            metronome(tempo)
            print("looping.")


            

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        audio.terminate()






    # try:
    #     while True:
    #         data = stream.read(CHUNK)
    #         bpm = process_audio(data)
    #         print(bpm)
    #         metronome(bpm)
    # except KeyboardInterrupt:
    #     print("\nStopping...")
    #     print("BPM: ", bpm)
    # finally:
    #     stream.stop_stream()
    #     stream.close()
    #     audio.terminate()

if __name__ == "__main__":
    main()
