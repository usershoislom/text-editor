import tkinter as tk
from tkinter import filedialog, font
from tkinter import ttk

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")
        self.last_opened_file = ""
        self.url = ''
        self.fontStyle = 'Arial'
        self.fontSize = 12

        self.create_menu()
        self.create_toolbar()
        self.create_text_editor()
        self.create_status_bar()

        self.bind_shortcuts()

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='New', accelerator='Ctrl+N', command=self.new_file)
        file_menu.add_command(label="Open", accelerator='Ctrl+O', command=self.open_file)
        file_menu.add_command(label="Save", accelerator='Ctrl+S', command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator='Ctrl+Q', command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=False)
        edit_menu.add_command(label='Undo', accelerator='Ctrl+Z', compound=tk.LEFT)
        edit_menu.add_command(label='Cut', accelerator='Ctrl+X', compound=tk.LEFT,
                              command=lambda: self.text_editor.event_generate('<Control x>'))
        edit_menu.add_command(label='Copy', accelerator='Ctrl+C', compound=tk.LEFT,
                              command=lambda: self.text_editor.event_generate('<Control c>'))
        edit_menu.add_command(label='Paste', accelerator='Ctrl+V', compound=tk.LEFT,
                              command=lambda: self.text_editor.event_generate('<Control v>'))
        edit_menu.add_command(label='Clear', accelerator='Ctrl+Alt+X', compound=tk.LEFT,
                              command=lambda: self.text_editor.delete(0.0, tk.END))
        edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound=tk.LEFT, command=self.find)
        self.menu_bar.add_cascade(label='Edit', menu=edit_menu)

        themes_menu = tk.Menu(self.menu_bar, tearoff=False)
        theme_choice = tk.StringVar()
        themes_menu.add_radiobutton(label='Light Default', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.change_theme('white', 'black'))
        themes_menu.add_radiobutton(label='Dark', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.change_theme('#a6ece0', '#544b3d'))
        themes_menu.add_radiobutton(label='Pink', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.change_theme('pink', 'blue'))
        themes_menu.add_radiobutton(label='Monokai', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.change_theme('orange', 'white'))
        self.menu_bar.add_cascade(label='Themes', menu=themes_menu)

        self.root.config(menu=self.menu_bar)

    def create_toolbar(self):
        self.tool_bar = tk.Label(self.root)
        self.tool_bar.pack(side=tk.TOP, fill=tk.X)

        font_families = font.families()
        self.font_family_variable = tk.StringVar()
        font_family_combobox = ttk.Combobox(self.tool_bar, width=30, values=font_families,
                                            state='readonly', textvariable=self.font_family_variable)
        font_family_combobox.current(font_families.index('Arial'))
        font_family_combobox.grid(row=0, column=0, padx=5)
        font_family_combobox.bind('<<ComboboxSelected>>', self.change_font_style)

        self.size_variable = tk.IntVar()
        font_size_combobox = ttk.Combobox(self.tool_bar, width=14, textvariable=self.size_variable,
                                          state='readonly', values=tuple(range(8, 81)))
        font_size_combobox.current(4)
        font_size_combobox.grid(row=0, column=1, padx=5)
        font_size_combobox.bind('<<ComboboxSelected>>', self.change_font_size)

    def create_text_editor(self):
        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_editor = tk.Text(self.root, yscrollcommand=self.scrollbar.set, font=(self.fontStyle, self.fontSize),
                                   undo=True)
        self.text_editor.pack(expand=True, fill="both")

        self.scrollbar.config(command=self.text_editor.yview)

        self.text_editor.bind('<<Modified>>', self.update_status_bar)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text='Status Bar')
        self.status_bar.pack(side=tk.BOTTOM)

    def bind_shortcuts(self):
        self.root.bind_all("<Control-s>", self.save_file)
        self.root.bind_all("<Control-q>", self.exit_editor)
        self.root.bind_all("<Control-o>", self.open_file)
        self.root.bind_all("<Control-u>", self.delete_line)
        self.root.bind_all("<Control-w>", self.delete_word)
        self.root.bind_all("<Control-n>", self.new_file)
        self.root.bind_all("<Control-f>", self.find)
        self.root.bind_all("<Home>", self.move_cursor)
        self.root.bind_all("<End>", self.move_cursor)

    def new_file(self, event=None):
        self.url = ''
        self.text_editor.delete(0.0, tk.END)
        self.root.title("Text Editor")

    def open_file(self, event=None):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "r") as file:
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert(tk.END, file.read())
                self.last_opened_file = filepath
                self.root.title(f"Text Editor - {filepath}")
        else:
            self.root.title("Text Editor")

    def save_file(self, event=None):
        if self.last_opened_file:
            with open(self.last_opened_file, "w") as file:
                file.write(self.text_editor.get("1.0", tk.END))
        else:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text Files", "*.txt")])
            if filepath:
                with open(filepath, "w") as file:
                    file.write(self.text_editor.get("1.0", tk.END))
                self.last_opened_file = filepath
                self.root.title(f"Text Editor - {filepath}")

    def exit_editor(self, event=None):
        self.root.quit()

    def move_cursor(self, event):
        if event.keysym == "Home":
            self.text_editor.mark_set(tk.INSERT, "1.0")
        elif event.keysym == "End":
            self.text_editor.mark_set(tk.INSERT, tk.END)

    def delete_line(self, event):
        self.text_editor.delete("insert linestart", "insert lineend+1c")

    def delete_word(self, event):
        start = self.text_editor.index("insert")
        while True:
            prev_char = self.text_editor.get(f"{start}")
            if prev_char == " " or start == "1.0":
                break
            start = self.text_editor.index(f"{start}-1c")
        self.text_editor.delete(start, "insert")

    def find(self):
        def find_words():
            self.text_editor.tag_remove('match', 1.0, tk.END)
            start_pos = '1.0'
            word = find_entry.get()
            if word:
                while True:
                    start_pos = self.text_editor.search(word, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f'{start_pos}+{len(word)}c'  # 1.0+1c
                    self.text_editor.tag_add('match', start_pos, end_pos)

                    self.text_editor.tag_config('match', foreground='red', background='yellow')
                    start_pos = end_pos

        def replace_text():
            word = find_entry.get()
            replace_word = replace_entry.get()
            content = self.text_editor.get(1.0, tk.END)
            new_content = content.replace(word, replace_word)
            self.text_editor.delete(1.0, tk.END)
            self.text_editor.insert(1.0, new_content)

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
            self.text_editor.tag_remove('match', 1.0, tk.END)
            root1.destroy()

        root1.protocol('WM_DELETE_WINDOW', do_something)
        root1.mainloop()

    def change_font_style(self, event):
        self.fontStyle = self.font_family_variable.get()
        self.text_editor.config(font=(self.fontStyle, self.fontSize))

    def change_font_size(self, event):
        self.fontSize = self.size_variable.get()
        self.text_editor.config(font=(self.fontStyle, self.fontSize))

    def update_status_bar(self, event):
        words = len(self.text_editor.get(0.0, tk.END).split())
        characters = len(self.text_editor.get(0.0, 'end-1c').replace(' ', ''))
        self.status_bar.config(text=f'Characters: {characters} Words: {words}')
        self.text_editor.edit_modified(False)

    def change_theme(self, bg_color, fg_color):
        self.text_editor.config(bg=bg_color, fg=fg_color)

    def run(self):
        self.root.mainloop()

text_editor = TextEditor()
text_editor.run()
