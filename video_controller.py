import cv2
import os

def play_video(file_path):
    """
    Play the video located at file_path.
    """
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print(f"Error opening video file: {file_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or check_trigger():
            break  # Break the loop if the video ends or the trigger is activated

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def check_trigger():
    """
    Check for a specific key press to act as a trigger.
    Replace this with your trigger logic later.
    """
    return cv2.waitKey(1) & 0xFF == ord('n')  # Press 'n' to switch to the next video

def main():
    video_folder = 'C:\Users\ecoli\OneDrive\Desktop\local_repositories\live_music_audio_visualizer\frames'  # Change to your video folder path
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi'))]  # Add other formats if needed
    video_files.sort()  # Sort the files if needed

    for video_file in video_files:
        video_path = os.path.join(video_folder, video_file)
        play_video(video_path)

if __name__ == "__main__":
    main()
