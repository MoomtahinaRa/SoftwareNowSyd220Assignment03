import tkinter as tk
from tkinter import ttk
from transformers import MarianMTModel, MarianTokenizer

# Step 1: Initialize the model and tokenizer for language translation
def load_model(source_lang, target_lang):
    model_name = f'Helsinki-NLP/opus-mt-{source_lang}-{target_lang}'
    model = MarianMTModel.from_pretrained(model_name)
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    return model, tokenizer

# Step 2: Translate text using the AI model
def translate_text():
    source_lang = source_lang_var.get()  # Get the source language from the dropdown
    target_lang = target_lang_var.get()  # Get the target language from the dropdown
    input_text = input_box.get("1.0", "end").strip()  # Get the text from the input box

    try:
        # Load the model and tokenizer
        model, tokenizer = load_model(source_lang, target_lang)

        # Tokenize the input
        tokenized_input = tokenizer(input_text, return_tensors="pt", padding=True)

        # Generate translation
        translated_output = model.generate(**tokenized_input)
        translated_text = tokenizer.decode(translated_output[0], skip_special_tokens=True)

        # Display translation in the output text box
        output_box.config(state=tk.NORMAL)  # Enable editing in output box
        output_box.delete("1.0", tk.END)  # Clear previous content
        output_box.insert(tk.END, translated_text)  # Insert new translation
        output_box.config(state=tk.DISABLED)  # Disable editing in output box

    except Exception as e:
        output_box.config(state=tk.NORMAL)
        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Error: {str(e)}")
        output_box.config(state=tk.DISABLED)

# Step 3: Set up the Tkinter interface
app = tk.Tk()
app.title("Language Translation App")

# Input Text Label and Box
input_label = tk.Label(app, text="Enter text to translate:")
input_label.pack()

input_box = tk.Text(app, height=5, width=50)
input_box.pack()

# Language Selection
source_lang_var = tk.StringVar(value="en")
target_lang_var = tk.StringVar(value="fr")

source_lang_label = tk.Label(app, text="Source Language:")
source_lang_label.pack()

source_lang_menu = ttk.Combobox(app, textvariable=source_lang_var)
source_lang_menu['values'] = ("en", "es", "de", "fr", "it")
source_lang_menu.pack()

target_lang_label = tk.Label(app, text="Target Language:")
target_lang_label.pack()

target_lang_menu = ttk.Combobox(app, textvariable=target_lang_var)
target_lang_menu['values'] = ("en", "es", "de", "fr", "it")
target_lang_menu.pack()

# Translate Button
translate_button = tk.Button(app, text="Translate", command=translate_text)
translate_button.pack()

# Output Text Label and Box
output_label = tk.Label(app, text="Translated text:")
output_label.pack()

output_box = tk.Text(app, height=5, width=50, state=tk.DISABLED)
output_box.pack()

# Run the Tkinter event loop
app.mainloop()
