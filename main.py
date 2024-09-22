import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageSequence
import os

def extract_frames():
    file_path = filedialog.askopenfilename(filetypes=[("GIF Files", "*.gif")])
    if not file_path:
        return

    output_dir = os.path.join(os.path.dirname(__file__), "frames")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    try:
        img = Image.open(file_path)
        duration = img.info.get('duration', 100)  # Get the frame duration from the GIF, default 100ms
        for i, frame in enumerate(ImageSequence.Iterator(img)):
            frame.save(os.path.join(output_dir, f"frame_{i}.png"))
        messagebox.showinfo("Success", f"Frames extracted to {output_dir}. Frame duration: {duration}ms")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to extract frames: {str(e)}")

def combine_to_gif():
    file_paths = filedialog.askopenfilenames(filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg")])
    if not file_paths:
        return

    output_file = filedialog.asksaveasfilename(defaultextension=".gif", filetypes=[("GIF Files", "*.gif")])
    if not output_file:
        return

    try:
        delay = int(delay_entry.get())  # Get the delay from the entry box

        frames = [Image.open(file) for file in file_paths]
        frames[0].save(output_file, save_all=True, append_images=frames[1:], loop=0, duration=delay)
        messagebox.showinfo("Success", f"GIF created: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to create GIF: {str(e)}")

root = tk.Tk()
root.title("GIF Frame Extractor & Combiner")
root.geometry("400x300")

extract_btn = tk.Button(root, text="Extract Frames from GIF", command=extract_frames)
extract_btn.pack(pady=20)

tk.Label(root, text="Delay between frames (ms):").pack()
delay_entry = tk.Entry(root)
delay_entry.pack(pady=10)
delay_entry.insert(0, "100")  # Default delay is set to 100ms

combine_btn = tk.Button(root, text="Combine Images to GIF", command=combine_to_gif)
combine_btn.pack(pady=20)

root.mainloop()
