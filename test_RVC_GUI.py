import tkinter as tk
from tkinter import ttk
import os
import sys

import soundfile as sf

now_dir = os.getcwd()
sys.path.append(now_dir)
import test_RVC


def submit():
    name = name_entry.get()
    input_path = input_path_entry.get()
    model_file = model_combobox.get()
    index_file = index_combobox.get()
    f0method = f0method_combobox.get()

    # Perform further actions with the collected data
    print("Name:", name)
    print("Input Path:", input_path)
    print("Model File:", model_file)
    print("Index File:", index_file)
    print("f0method:", f0method)
    audio = test_RVC.Run_RVC(input_path, f0method, model_file, index_file)
    tgt_sr, audio_opt = audio

    # Check if the directory "Outputs" exists, if not, create it
    if not os.path.exists("Outputs"):
        os.makedirs("Outputs")

    sf.write(
        "%s/%s.%s" % ("Outputs", name, "wav"),
        audio_opt,
        tgt_sr,
    )



root = tk.Tk()
root.title("Amazing GUI")
root.geometry("400x300")

# Styling
style = ttk.Style()
style.configure('TLabel', background='#d9efff')
style.configure('TFrame', background='#d9efff')
style.configure('TButton', background='#ffb3b3')

# Name
name_label = ttk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

# Input Path
input_path_label = ttk.Label(root, text="Input Path:")
input_path_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
input_path_entry = ttk.Entry(root)
input_path_entry.grid(row=1, column=1, padx=10, pady=10)

# Model File
model_label = ttk.Label(root, text="Model File:")
model_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
model_combobox = ttk.Combobox(root, values=test_RVC.models_names)
model_combobox.grid(row=2, column=1, padx=10, pady=10)

# Index File
index_label = ttk.Label(root, text="Index File:")
index_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
index_combobox = ttk.Combobox(root, values=test_RVC.index_paths)
index_combobox.grid(row=3, column=1, padx=10, pady=10)

# f0method
f0method_label = ttk.Label(root, text="f0 method:")
f0method_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
f0method_combobox = ttk.Combobox(root, values=["pm", "harvest", "crepe", "rmvpe"])
f0method_combobox.grid(row=4, column=1, padx=10, pady=10)

# Submit Button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(row=5, columnspan=2, padx=10, pady=10)

root.mainloop()
