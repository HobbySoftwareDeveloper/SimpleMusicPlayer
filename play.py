import os
import pygame
import time
import random
import sys
import numpy as np
from pydub import AudioSegment


# Initialize pygame mixer
print("Initializing \"PyGame\"")
pygame.mixer.init()

# Function to clear the screen (works for Windows, macOS, and Linux)
def clear_screen():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS/Linux
        os.system('clear')

print("Searching for music files (.mp3, .wav, .ogg)")
# Get all music files in the current directory
music_files = [f for f in os.listdir('.') if f.endswith(('.mp3', '.wav', '.ogg'))]

# Function to format time in minutes and seconds
def format_time(seconds):
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02}:{secs:02}"

# Function to print a progress bar with time
def print_progress_bar(iteration, total, elapsed_time, total_time, length=60):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = '-' * filled_length + ' ' * (length - filled_length)
    return f"\r|{bar}| {percent}% {elapsed_time} / {total_time}"

# Function to create a dancing line based on volume
def dancing_line(volume):
    # Calculate the length of the dancing line based on volume
    beat_length = int(volume * 100)  # Scale volume from 0 to 1 to line length from 0 to 20
    dancing_line = "|" + "*" * beat_length 
    return dancing_line

# Function to get the current RMS volume of the audio
def get_rms_volume(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    # If stereo, average both channels
    if audio_segment.channels == 2:
        samples = samples.reshape((-1, 2)).mean(axis=1)
    rms = np.sqrt(np.mean(samples ** 2))  # Calculate RMS
    return rms

def play_music(music_list):
    random.shuffle(music_list)  # Shuffle the music list
    
    for music in music_list:
        if os.path.exists(music):
            clear_screen()
            
            # Load the music file using pydub
            audio = AudioSegment.from_file(music)
            total_length = len(audio) / 1000  # Length in seconds
            print(f"Now Playing: {music}")

            # Start playback
            pygame.mixer.music.load(music)
            pygame.mixer.music.play()

            start_time = time.time()
            while pygame.mixer.music.get_busy():
                elapsed_time_seconds = time.time() - start_time
                formatted_elapsed_time = format_time(elapsed_time_seconds)
                
                # Generate the progress bar
                progress_bar = print_progress_bar(elapsed_time_seconds, total_length, formatted_elapsed_time, format_time(total_length))

                # Get a segment of audio and calculate its RMS volume
                segment_start = int(elapsed_time_seconds * 1000)  # in milliseconds
                segment_end = segment_start + 100  # analyze 100ms of audio
                audio_segment = audio[segment_start:segment_end]
                rms_volume = get_rms_volume(audio_segment)

                # Normalize RMS volume to be between 0 and 1 for the dancing line
                normalized_volume = min(rms_volume / 32768.0, 1)  # 32768 is max for 16-bit audio
                vol_line = dancing_line(normalized_volume)

                # Clear the screen and print everything together
                clear_screen()
                print(f"Now Playing: {music}")
                print(progress_bar)
                print(vol_line)
                
                time.sleep(0.1)  # Update progress every 0.1 seconds
            
            print()  # Move to the next line after the progress bar
        else:
            print(f"File not found: {music}")

# Start playing music if there are any music files
if music_files:
    play_music(music_files)
else:
    print("No music files found in the current directory.")

# Clean up
pygame.mixer.quit()
