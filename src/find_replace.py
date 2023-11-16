import tkinter as tk

class FindReplace:
    def __init__(self, text_editor):
        self.text_editor = text_editor

    def find(self):
        def find_words():
            self.text_editor.text_editor.tag_remove('match', 1.0, tk.END)
            start_pos = '1.0'
            word = find_entry.get()
            if word:
                while True:
                    start_pos = self.text_editor.text_editor.search(word, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f'{start_pos}+{len(word)}c'  # 1.0+1c
                    self.text_editor.text_editor.tag_add('match', start_pos, end_pos)

                    self.text_editor.text_editor.tag_config('match', foreground='red', background='yellow')
                    start_pos = end_pos

        def replace_text():
            word = find_entry.get()
            replace_word = replace_entry.get()
            content = self.text_editor.text_editor.get(1.0, tk.END)
            new_content = content.replace(word, replace_word)
            self.text_editor.text_editor.delete(1.0, tk.END)
            self.text_editor.text_editor.insert(1.0, new_content)

        root1 = tk.Toplevel()
        root1.title('Find')
        root1.geometry('450x250+500+200')
        root1.resizable(0, 0)

        label_frame = tk.LabelFrame(root1, text='Find/Replace')
        label_frame.pack(pady=50)

        find_label = tk.Label(label_frame, text='Find')
        find_label.grid(row=0, column=0, padx=5, pady=5)
        find_entry = tk.Entry(label_frame)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        replace_label = tk.Label(label_frame, text='Replace')
        replace_label.grid(row=1, column=0, padx=5, pady=5)
        replace_entry = tk.Entry(label_frame)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        find_button = tk.Button(label_frame, text='FIND', command=find_words)
        find_button.grid(row=2, column=0, padx=5, pady=5)

        replace_button = tk.Button(label_frame, text='REPLACE', command=replace_text)
        replace_button.grid(row=2, column=1, padx=5, pady=5)

        def do_something():
            self.text_editor.text_editor.tag_remove('match', 1.0, tk.END)
            root1.destroy()

        root1.protocol('WM_DELETE_WINDOW', do_something)
        root1.mainloop()

    def change_font_style(self, event):
        self.text_editor.fontStyle = self.text_editor.font_family_variable.get()
        self.text_editor.text_editor.tag_configure('font', font=(self.text_editor.fontStyle, self.text_editor.fontSize))
        self.text_editor.text_editor.tag_add('font', 1.0, tk.END)

    def change_font_size(self, event):
        self.text_editor.fontSize = self.text_editor.size_variable.get()
        self.text_editor.text_editor.tag_configure('font', font=(self.text_editor.fontStyle, self.text_editor.fontSize))
        self.text_editor.text_editor.tag_add('font', 1.0, tk.END)

    def delete_line(self, event):
        self.text_editor.text_editor.delete("insert linestart", "insert lineend+1c")

    def delete_word(self, event):
        start = self.text_editor.text_editor.index("insert")
        while True:
            prev_char = self.text_editor.text_editor.get(f"{start}")
            if prev_char == " " or start == "1.0":
                break
            start = self.text_editor.text_editor.index(f"{start}-1c")
        self.text_editor.text_editor.delete(start, "insert")

    def move_cursor(self, event):
        if event.keysym == "Home":
            self.text_editor.text_editor.mark_set(tk.INSERT, "1.0")
        elif event.keysym == "End":
            self.text_editor.text_editor.mark_set(tk.INSERT, tk.END)

    def update_status_bar(self, event):
        words = len(self.text_editor.text_editor.get(0.0, tk.END).split())
        characters = len(self.text_editor.text_editor.get(0.0, 'end-1c').replace(' ', ''))
        self.text_editor.status_bar.config(text=f'Characters: {characters} Words: {words}')
        self.text_editor.text_editor.edit_modified(False)
