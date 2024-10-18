import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import tensorflow as tf
import numpy as np
import os
import certifi
os.environ['SSL_CERT_FILE'] = certifi.where()

# Multiple inheritance: This class inherits from both Tkinter Frame and object
class ImageClassifierApp(tk.Frame):

    def __init__(self, parent=None):
        # Encapsulation: __model is a private attribute
        self.__model = None  
        self.load_model()  # Load the AI model

        # Initialize the Frame class (Superclass constructor)
        super().__init__(parent)  # Calling the Frame superclass constructor
        self.parent = parent
        self.setup_gui()

    # Method overriding: Overriding the parent's setup method
    def setup_gui(self):
        """Create the user interface."""
        self.parent.title("AI Image Classifier")

        # Label to display the selected image
        self.image_label = tk.Label(self.parent, text="Upload an image", width=50, height=10)
        self.image_label.pack(pady=10)

        # Button to upload the image
        self.upload_button = tk.Button(self.parent, text="Upload Image", command=self.upload_image)
        self.upload_button.pack(pady=5)

        # Button to classify the image
        self.classify_button = tk.Button(self.parent, text="Classify Image", command=self.classify_image)
        self.classify_button.pack(pady=5)

        # Label to display the classification result
        self.result_label = tk.Label(self.parent, text="", width=50, height=2)
        self.result_label.pack(pady=10)

    # Multiple decorators: Static method, no access to instance or class
    @staticmethod
    def preprocess_image(image_path):
        """Preprocess the image for MobileNetV2."""
        image = Image.open(image_path)
        image = image.resize((224, 224))
        img_array = np.array(image)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        return img_array

    # Polymorphism: Classify function will work on any image passed to it
    def classify_image(self):
        """Classify the uploaded image using MobileNetV2."""
        if hasattr(self, 'file_path') and self.file_path:
            img_array = self.preprocess_image(self.file_path)
            predictions = self.__model.predict(img_array)
            predicted_class = np.argmax(predictions[0])
            labels = ['Cat', 'Dog', 'Bird', 'Other']  # Simplified example labels
            self.result_label.config(text=f"Prediction: {labels[predicted_class]}")
        else:
            messagebox.showerror("Error", "No image uploaded")

    # Method overriding: Overriding the method to provide custom functionality
    def upload_image(self):
        """Handle image uploading."""
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path = file_path  # Saving file path to be used in classify_image
            img = Image.open(file_path)
            img = img.resize((200, 200))
            img = ImageTk.PhotoImage(img)
            self.image_label.config(image=img)
            self.image_label.image = img  # Prevent garbage collection
        else:
            messagebox.showwarning("Warning", "No file selected")

    # Encapsulation: Private method to load the AI model
    def load_model(self):
        """Load MobileNetV2 AI model for image classification."""
        # Multiple decorators: Classmethod decorator to show static usage in practice
        @classmethod
        def _load_pretrained_model(cls):
            return tf.keras.applications.MobileNetV2(weights='imagenet', include_top=False)
        
        # Load MobileNetV2 model with weights from ImageNet dataset
        self.__model = tf.keras.applications.MobileNetV2(weights='imagenet')
        print("AI Model Loaded Successfully!")


# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClassifierApp(root)
    root.geometry("500x400")
    root.mainloop()
