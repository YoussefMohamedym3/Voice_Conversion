import os
import subprocess
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

def video_to_wav(video_path, output_folder):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Extract filename without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Load video clip
    video_clip = VideoFileClip(video_path)

    # Set output wav file path
    wav_output_path = os.path.join(output_folder, f"{video_name}.wav")

    # Write audio from video clip to wav file
    video_clip.audio.write_audiofile(wav_output_path)

    print(f"Video converted to WAV successfully: {wav_output_path}")


def run_test_RVC(input_wav_path, f0_method, model_path, index_path):
    # Define the path to the Python interpreter and the script to run
    python_executable = 'runtime\\python.exe'
    script_file = 'test_RVC.py'

    # Define the command to run the script
    command = [
        python_executable,
        script_file,
        (str)(input_wav_path),
        (str)(f0_method),
        (str)(model_path),
        (str)(index_path)
    ]

    # Run the script using the specified Python interpreter
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # Input video path
    video_folder = "user_video"
    video_file = "example_video.mp4"  # Change this to your video file name

    # Output folder
    output_folder = "rvc_input"

    # Full video path
    video_path = os.path.join(video_folder, video_file)

    # Convert video to wav
    video_to_wav(video_path, output_folder)

    # Input WAV file path
    input_wav_path = os.path.join(output_folder, "example_video.wav")

    # Parameters for Run_RVC function
    f0_method = "pm"
    model_path = "SpongeBobSquarePants.pth"
    index_path = "logs/added_IVF3536_Flat_nprobe_1_v2.index"

    # Run Run_RVC function
    run_test_RVC(input_wav_path, f0_method, model_path, index_path)

    

    # Load video and audio files
    video = VideoFileClip("character_video\example_video.mp4")
    audio = AudioFileClip("Outputs/name.wav")

    # Set the audio of the video file
    video = video.set_audio(audio)

    # Define the output directory
    output_directory = "final_result"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Specify the output file path
    output_path = os.path.join(output_directory, "combined_video.mp4")

    # Write the result to the output file
    video.write_videofile(output_path, codec="libx264", audio_codec="aac")

