import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageScaler:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Scaler")

        # Create a button to select an image file
        self.select_button = tk.Button(self.master, text="Select Image", command=self.select_image)
        self.select_button.pack()

        # Create a dropdown menu to choose the scaling factor
        self.scale_var = tk.StringVar(value="0.5")
        self.scale_menu = tk.OptionMenu(self.master, self.scale_var, "0.25", "0.5", "0.75")
        self.scale_menu.pack()

        # Create a button to downscale the image
        self.downscale_button = tk.Button(self.master, text="Downscale", command=self.downscale_image)
        self.downscale_button.pack()

        # Create a button to upscale the image
        self.upscale_button = tk.Button(self.master, text="Upscale", command=self.upscale_image)
        self.upscale_button.pack()

        # Create a label to display the image
        self.image_label = tk.Label(self.master)
        self.image_label.pack()

    def select_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename()

        # Load the image and display it in the label
        self.image = Image.open(file_path)
        self.photo = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=self.photo)

    def downscale_image(self):
        # Get the current size of the image
        width, height = self.image.size

        # Calculate the new size based on the user's choice
        scale_factor = float(self.scale_var.get())
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Downscale the image using the Lanczos algorithm
        resized_image = self.image.resize((new_width, new_height), resample=Image.LANCZOS)

        # Display the modified image in the label
        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.photo)

    def upscale_image(self):
        # Get the current size of the image
        width, height = self.image.size

        # Calculate the new size based on the user's choice
        scale_factor = float(self.scale_var.get())
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)

        # Upscale the image using the bicubic algorithm
        resized_image = self.image.resize((new_width, new_height), resample=Image.BICUBIC)

        # Display the modified image in the label
        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.photo)

root = tk.Tk()
app = ImageScaler(root)
root.mainloop()
