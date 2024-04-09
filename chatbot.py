from openai import OpenAI
from pathlib import Path
# import sounddevice as sd
# import soundfile as sf
import os
import speech_recognition as sr
from dotenv import load_dotenv
import subprocess  # Import subprocess module for running external scripts
from moviepy.editor import VideoFileClip
from moviepy.editor import AudioFileClip

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)
personality = "You are a teacher for children aged 5 to 10."
messages = [{"role": "system", "content": f"{personality}"}]

# def generate_audio(text):
#     speech_file_path = Path(__file__).parent / "speech.mp3"
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="nova",
#         input=text
#     )
#     response.stream_to_file(speech_file_path)
#     audio_data, sample_rate = sf.read(speech_file_path)
#     sd.play(audio_data, sample_rate)
#     sd.wait()

# Experiment with different voices (alloy, echo, fable, onyx, nova, and shimmer) 
# def generate_audio(text):
#     speech_file_path = Path(__file__).parent / "teacherResponse.wav"  # Change file extension to .wav
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="echo",
#         input=text
#     )
#     response.stream_to_file(speech_file_path)


def generate_audio(text):
    output_folder = Path(__file__).parent / "gpt_response"
    output_folder.mkdir(parents=True, exist_ok=True)  # Create the folder if it doesn't exist

    speech_file_path = output_folder / "teacherResponse.wav"  # Change file path to be inside the folder
    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=text
    )
    response.stream_to_file(speech_file_path)


    # # Read the audio data and sample rate from the .wav file
    # audio_data, sample_rate = sf.read(speech_file_path)
    
    # # Play the audio
    # sd.play(audio_data, sample_rate)
    # sd.wait()

    # Optionally, you can write the audio data to a .wav file
    # sf.write("output.wav", audio_data, sample_rate)  # Uncomment this line if you want to write the audio to a .wav file


def generate_text():
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    print(response.choices[0].message.content)

    bot_response = response.choices[0].message.content
    messages.append({"role": "assistant", "content": f"{bot_response}"})
    return bot_response

def listen_and_recognize():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio)
        print("You said:", query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return None

# def listen_and_recognize():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)

#     try:
#         print("Recognizing...")
#         query = recognizer.recognize_google(audio)
#         print("You said:", query)
#         if "bye bye teacher" in query.lower():
#             print("Exiting...")
#             return "bye bye teacher"
#         else:
#             return query
#     except sr.UnknownValueError:
#         print("Sorry, I couldn't understand what you said.")
#         return None
#     except sr.RequestError as e:
#         print("Could not request results from Google Speech Recognition service; {0}".format(e))
#         return None



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

def main():
    
    user_input = listen_and_recognize()
    if user_input:
        messages.append({"role": "user", "content": user_input})
        bot_response = generate_text()
        generate_audio(bot_response)

    # Input WAV file path
    input_wav_path = os.path.join("gpt_response", "teacherResponse.wav")

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
if __name__ == "__main__":
    main()

# def main():
#     while True:
#         user_input = listen_and_recognize()
#         if user_input:
#             if user_input == "bye bye teacher":
#                 break  # Exit the loop if the user says "bye bye teacher"
#             messages.append({"role": "user", "content": user_input})
#             bot_response = generate_text()
#             generate_audio(bot_response)
#             run_test_RVC()  # Call the function to run test_RVC()

#     print("Goodbye!")  # Print a goodbye message before exiting

# if __name__ == "__main__":
#     main()



