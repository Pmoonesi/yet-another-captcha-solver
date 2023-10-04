from PIL import ImageTk, Image
from tkinter import END
import tkinter as tk
import os
import sys

if len(sys.argv) < 3:
    print('not enough arguments')
    exit(-1)

try:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
except Exception as e:
    print('could not parse arguments.')
    exit(-1)

# List of image paths
image_paths = os.listdir('data/')
current_image_no = start

def update_image():
    global current_image_no
    current_image_no += 1
    if current_image_no > end:
        exit(-1)
    # if current_image_no % 100 == 0:
    #     print(f'current label number: {current_image_no}')
    image = Image.open(os.path.join('data/', f'{current_image_no}.png'))
    image_tk = ImageTk.PhotoImage(image)
    label.configure(image=image_tk)
    label.image = image_tk  # Update the reference to avoid garbage collection

def on_button_click():
    input_text = entry.get()
    print(f"{current_image_no}\tUser input:", input_text)
    with open(f'new_label/{current_image_no}.txt', 'w') as f:
        f.write(f'{input_text}')
    entry.delete(0, END)
    update_image()

def on_enter_press(event):
    on_button_click()

# Create a Tkinter window
window = tk.Tk()

# Create an ImageTk object for the initial image
image = Image.open(os.path.join('data/', f'{current_image_no}.png'))
image_tk = ImageTk.PhotoImage(image)

# Create a Tkinter label and set it as the image
label = tk.Label(window, image=image_tk)
label.pack()

# Create a Tkinter entry widget for user input
entry = tk.Entry(window)
entry.pack()

# Create a Tkinter button to trigger user input retrieval
button = tk.Button(window, text="Submit", command=on_button_click)
button.pack()

# Bind the <Return> event (Enter key press) to the button
window.bind('<Return>', on_enter_press)

# Start the Tkinter event loop
window.mainloop()
