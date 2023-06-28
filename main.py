import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageScaler:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Scaler")
        self.master.geometry("1280x720")

        # Create a button to select an image file
        self.select_button = tk.Button(self.master, text="Select Image", command=self.select_image)
        self.select_button.pack(side="top", fill="both", expand=True)

        # Create a dropdown menu to choose the scaling factor
        self.scale_var = tk.StringVar(value="0.5")
        self.scale_menu = tk.OptionMenu(self.master, self.scale_var, "0.25", "0.5", "0.75")
        self.scale_menu.pack(side="top", fill="both", expand=True)

        # Create a button to downscale the image
        self.downscale_button = tk.Button(self.master, text="Downscale", command=self.downscale_image)
        self.downscale_button.pack(side="top", fill="both", expand=True)

        # Create a button to upscale the image
        self.upscale_button = tk.Button(self.master, text="Upscale", command=self.upscale_image)
        self.upscale_button.pack(side="top", fill="both", expand=True)

        # Create a button to save the modified image
        self.save_button = tk.Button(self.master, text="Save Image", command=self.save_image)
        self.save_button.pack(side="top", fill="both", expand=True)

        # Create a label to display the image
        self.image_label = tk.Label(self.master)
        self.image_label.pack(side="top", fill="both", expand=True)

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

        # Downscale the image using bicubic interpolation
        resized_image = self.image.resize((new_width, new_height), resample=Image.BICUBIC)

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

        # Upscale the image using bicubic interpolation
        resized_image = self.image.resize((new_width, new_height), resample=Image.BICUBIC)

        # Display the modified image in the label
        self.photo = ImageTk.PhotoImage(resized_image)
        self.image_label.config(image=self.photo)

    def save_image(self):
        # Open a file dialog to select a file name and location to save the image
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg")

        # Save the modified image to the selected file with the appropriate file extension
        file_extension = file_path.split(".")[-1].lower()
        if file_extension == "jpg":
            self.image.save(file_path, "JPEG")
        elif file_extension == "png":
            self.image.save(file_path, "PNG")
        else:
            # Default to JPEG if the file extension is not recognized
            self.image.save(file_path, "JPEG")

root = tk.Tk()
app = ImageScaler(root)
root.mainloop()
