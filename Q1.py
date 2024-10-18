import tkinter as tk
from transformers import MarianMTModel, MarianTokenizer

# Load the MarianMT model and tokenizer for translation
def load_model(src_lang, tgt_lang):
    model_name = f'Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}'
    tokenizer = MarianTokenizer.from_pretrained(model_name)
    model = MarianMTModel.from_pretrained(model_name)
    return tokenizer, model

# Translation function
def translate_text():
    input_text = input_box.get("1.0", "end-1c")
    src_lang = src_lang_var.get()
    tgt_lang = tgt_lang_var.get()

    tokenizer, model = load_model(src_lang, tgt_lang)
    translated = model.generate(**tokenizer.prepare_seq2seq_batch([input_text], return_tensors="pt"))
    output_text = tokenizer.decode(translated[0], skip_special_tokens=True)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output_text)

# Set up the GUI
root = tk.Tk()
root.title("Language Translator")

# Input box
input_label = tk.Label(root, text="Enter Text:")
input_label.pack()
input_box = tk.Text(root, height=10, width=50)
input_box.pack()

# Dropdowns for language selection
src_lang_var = tk.StringVar(root)
tgt_lang_var = tk.StringVar(root)

src_lang_options = ['en', 'fr', 'de']  # Add other language codes here
tgt_lang_options = ['en', 'fr', 'de']  # Add other language codes here

src_lang_menu = tk.OptionMenu(root, src_lang_var, *src_lang_options)
src_lang_menu.pack()
tgt_lang_menu = tk.OptionMenu(root, tgt_lang_var, *tgt_lang_options)
tgt_lang_menu.pack()

# Translate button
translate_button = tk.Button(root, text="Translate", command=translate_text)
translate_button.pack()

# Output box
output_label = tk.Label(root, text="Translated Text:")
output_label.pack()
output_box = tk.Text(root, height=10, width=50)
output_box.pack()

root.mainloop()
