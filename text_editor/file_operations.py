from tkinter import filedialog, tk

class FileOperations:
    def __init__(self, text_editor):
        self.text_editor = text_editor

    def new_file(self, event=None):
        self.text_editor.url = ''
        self.text_editor.text_editor.delete(0.0, tk.END)
        self.text_editor.root.title("Text Editor")

    def open_file(self, event=None):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "r") as file:
                self.text_editor.text_editor.delete("1.0", tk.END)
                self.text_editor.text_editor.insert(tk.END, file.read())
                self.text_editor.last_opened_file = filepath
                self.text_editor.root.title(f"Text Editor - {filepath}")
        else:
            self.text_editor.root.title("Text Editor")

    def save_file(self, event=None):
        if self.text_editor.last_opened_file:
            with open(self.text_editor.last_opened_file, "w") as file:
                file.write(self.text_editor.text_editor.get("1.0", tk.END))
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text Files", "*.txt")])
            if filepath:
                with open(filepath, "w") as file:
                    file.write(self.text_editor.text_editor.get("1.0", tk.END))
                self.text_editor.last_opened_file = filepath
                self.text_editor.root.title(f"Text Editor - {filepath}")
