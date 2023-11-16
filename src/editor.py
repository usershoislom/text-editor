import tkinter as tk
import tkinter.messagebox as messagebox
# from language_config import LanguageConfig
from tkinter import filedialog, font, ttk
from file_operations import FileOperations
from find_replace import FindReplace
from theme_operations import ThemeOperations

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Text Editor")
        self.last_opened_file = ""
        self.url = ''
        self.fontStyle = 'Arial'
        self.fontSize = 12

        self.file_operations = FileOperations(self)
        self.find_replace = FindReplace(self)
        self.theme_operations = ThemeOperations(self)
        self.load_python_keywords()

        self.create_menu()
        self.create_toolbar()
        self.create_text_editor()
        self.create_status_bar()

        self.bind_shortcuts()
        # self.find_replace = None
        # self.theme_operations = None

    def create_menu(self):

        self.menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label='New', accelerator='Ctrl+N', command=self.file_operations.new_file)
        file_menu.add_command(label="Open", accelerator='Ctrl+O', command=self.file_operations.open_file)
        file_menu.add_command(label="Save", accelerator='Ctrl+S', command=self.file_operations.save_file)
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
        edit_menu.add_command(label='Find', accelerator='Ctrl+F', compound=tk.LEFT, command=self.find_replace.find)
        self.menu_bar.add_cascade(label='Edit', menu=edit_menu)

        themes_menu = tk.Menu(self.menu_bar, tearoff=False)
        theme_choice = tk.StringVar()
        themes_menu.add_radiobutton(label='Light', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.theme_operations.change_theme('white', 'black'))
        themes_menu.add_radiobutton(label='Blue', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.theme_operations.change_theme('#a6ece0', '#544b3d'))
        themes_menu.add_radiobutton(label='Pink', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.theme_operations.change_theme('pink', 'blue'))
        themes_menu.add_radiobutton(label='Monokai', variable=theme_choice, compound=tk.LEFT,
                                    command=lambda: self.theme_operations.change_theme('orange', 'white'))
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
        font_family_combobox.bind('<<ComboboxSelected>>', self.find_replace.change_font_style)

        self.size_variable = tk.IntVar()
        font_size_combobox = ttk.Combobox(self.tool_bar, width=14, textvariable=self.size_variable,
                                          state='readonly', values=tuple(range(8, 81)))
        font_size_combobox.current(4)
        font_size_combobox.grid(row=0, column=1, padx=5)
        font_size_combobox.bind('<<ComboboxSelected>>', self.find_replace.change_font_size)

    def create_text_editor(self):
        self.scrollbar = ttk.Scrollbar(self.root)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_editor = tk.Text(self.root, yscrollcommand=self.scrollbar.set, font=(self.fontStyle, self.fontSize),
                                   undo=True)
        self.text_editor.pack(expand=True, fill="both")

        self.scrollbar.config(command=self.text_editor.yview)

        self.text_editor.bind('<<Modified>>', self.find_replace.update_status_bar)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text='Status Bar')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def configure_status_bar(self, event):
        self.status_bar.pack_forget()
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_shortcuts(self):
        self.root.bind_all("<Control-s>", self.file_operations.save_file)
        self.root.bind_all("<Control-q>", self.exit_editor)
        self.root.bind_all("<Control-o>", self.file_operations.open_file)
        self.root.bind_all("<Control-u>", self.find_replace.delete_line)
        self.root.bind_all("<Control-w>", self.find_replace.delete_word)
        self.root.bind_all("<Control-n>", self.file_operations.new_file)
        self.root.bind_all("<Control-f>", self.find_replace.find)
        self.root.bind_all("<Home>", self.move_cursor)
        self.root.bind_all("<End>", self.move_cursor)

    def exit_editor(self, event=None):
        self.root.quit()

    def move_cursor(self, event):
        if event.keysym == "Home":
            self.text_editor.mark_set(tk.INSERT, "1.0")
        elif event.keysym == "End":
            self.text_editor.mark_set(tk.INSERT, tk.END)

    def update_status_bar(self, event):
        words = len(self.text_editor.get(0.0, tk.END).split())
        characters = len(self.text_editor.get(0.0, 'end-1c').replace(' ', ''))
        self.status_bar.config(text=f'Characters: {characters} Words: {words}')
        self.text_editor.edit_modified(False)

    def load_python_keywords(self):
        with open('python_keywords.txt', 'r') as file:
            self.python_keywords = set(file.read().split())

    def run(self):
        self.root.bind("<Configure>", self.configure_status_bar)
        self.root.mainloop()

if __name__ == "__main__":
    if 'text_editor' not in globals():
        text_editor = TextEditor()
        text_editor.run()
