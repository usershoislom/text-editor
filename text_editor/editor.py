import tkinter as tk
from tkinter import filedialog, font
from tkinter import ttk

last_opened_file = ""

url=''
def new_file(event=None):
    global url
    url=''
    text_editor.delete(0.0, tk.END)
    root.title("Text Editor")

def open_file(event=None):
    global last_opened_file
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r") as file:
            text_editor.delete("1.0", tk.END)
            text_editor.insert(tk.END, file.read())
            last_opened_file = filepath
            root.title(f"Text Editor - {filepath}")
    else:
        root.title("Text Editor")

def save_file(event=None):
    global last_opened_file
    if last_opened_file:
        with open(last_opened_file, "w") as file:
            file.write(text_editor.get("1.0", tk.END))
    else:
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, "w") as file:
                file.write(text_editor.get("1.0", tk.END))
            last_opened_file = filepath
            root.title(f"Text Editor - {filepath}")  # Обновление заголовка окна с названием файла

def exit_editor(event=None):
    root.quit()

def move_cursor(event):
    if event.keysym == "Home":
        text_editor.mark_set(tk.INSERT, "1.0")
    elif event.keysym == "End":
        text_editor.mark_set(tk.INSERT, tk.END)

def delete_line(event):
    text_editor.delete("insert linestart", "insert lineend+1c")

def delete_word(event):
    start = text_editor.index("insert")
    while True:
        prev_char = text_editor.get(f"{start}")
        if prev_char == " " or start == "1.0":
            break
        start = text_editor.index(f"{start}-1c")
    text_editor.delete(start, "insert")

def find():
    def find_words():
        text_editor.tag_remove('match', 1.0, tk.END)
        start_pos = '1.0'
        word = findentryField.get()
        if word:
            while True:
                start_pos = text_editor.search(word,start_pos, stopindex = tk.END)
                if not start_pos:
                    break
                end_pos = f'{start_pos}+{len(word)}c' #1.0+1c
                text_editor.tag_add('match',start_pos,end_pos)

                text_editor.tag_config('match',foreground='red',background='yellow')
                start_pos=end_pos

    def replace_text():
        word = findentryField.get()
        replaceword = replaceentryField.get()
        content = text_editor.get(1.0, tk.END)
        new_content = content.replace(word, replaceword)
        text_editor.delete(1.0, tk.END)
        text_editor.insert(1.0, new_content)
        

    root1 = tk.Toplevel()
    root1.title('Find')
    root1.geometry('450x250+500+200')
    root1.resizable(0,0)

    labelFrame = tk.LabelFrame(root1,text='Find/Replace')
    labelFrame.pack(pady=50)

    findLabel = tk.Label(labelFrame,text='Find')
    findLabel.grid(row=0,column=0,padx=5,pady=5)
    findentryField = tk.Entry(labelFrame)
    findentryField.grid(row=0,column=1,padx=5,pady=5)

    replaceLabel = tk.Label(labelFrame, text='Replace')
    replaceLabel.grid(row=1, column=0, padx=5, pady=5)
    replaceentryField = tk.Entry(labelFrame)
    replaceentryField.grid(row=1, column=1, padx=5, pady=5)

    findButton = tk.Button(labelFrame,text='FIND',command=find_words)
    findButton.grid(row=2,column=0,padx=5,pady=5)

    replaceButton = tk.Button(labelFrame, text='REPLACE',command=replace_text)
    replaceButton.grid(row=2, column=1, padx=5, pady=5)

    def doSomething():
        text_editor.tag_remove('match', 1.0, tk.END)
        root1.destroy()

    root1.protocol('WM_DELETE_WINDOW', doSomething)
    root1.mainloop()

fontSize = 12
fontStyle = 'arial'
def font_style(event):
    global fontStyle
    fontStyle = font_family_variable.get()
    text_editor.config(font=(fontStyle, fontSize))

def font_size(event):
    global fontSize
    fontSize = size_variable.get()
    text_editor.config(font=(fontStyle, fontSize))

def statusBarFunction(event):
    words = len(text_editor.get(0.0, tk.END).split())
    characters = len(text_editor.get(0.0,'end-1c').replace(' ','')) #1.0
    status_bar.config(text=f'Charecters: {characters} Words: {words}')
    text_editor.edit_modified(False)

def change_theme(bg_color, fg_color):
    text_editor.config(bg=bg_color, fg=fg_color)

root = tk.Tk()
root.title("Text Editor")
# root.resizable(False, False)

menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label='New', accelerator='Ctrl+N', command=new_file)
file_menu.add_command(label="Open", accelerator='Ctrl+O', command=open_file)
file_menu.add_command(label="Save", accelerator='Ctrl+S', command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator='Ctrl+Q', command=root.quit)


menu_bar.add_cascade(label="File", menu=file_menu)


tool_bar = tk.Label(root)
tool_bar.pack(side=tk.TOP,fill=tk.X)
font_families = font.families()
font_family_variable = tk.StringVar()
fontfamily_Combobox = ttk.Combobox(tool_bar, width=30, values=font_families, state='readonly', textvariable=font_family_variable)
fontfamily_Combobox.current(font_families.index('Arial'))
fontfamily_Combobox.grid(row=0, column=0, padx=5)
size_variable = tk.IntVar()
font_size_Combobox = ttk.Combobox(tool_bar, width=14, textvariable=size_variable, state='readonly', values=tuple(range(8,81)))
font_size_Combobox.current(4)
font_size_Combobox.grid(row=0, column=1, padx=5)

fontfamily_Combobox.bind('<<ComboboxSelected>>',font_style)
font_size_Combobox.bind('<<ComboboxSelected>>',font_size)

# Создание поля для ввода текста
scrollbar = ttk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

img = tk.PhotoImage(file='/home/shoislom/python-projects/text_editor/img1.png')

text_editor = tk.Text(root, yscrollcommand=scrollbar.set, font=('arial',12), undo=True)
text_editor.pack(expand=True, fill="both")

scrollbar.config(command=text_editor.yview)
status_bar = ttk.Label(root,text='Status Bar')
status_bar.pack(side=tk.BOTTOM)
text_editor.bind('<<Modified>>', statusBarFunction)
#edit menu bar
edit_menu = tk.Menu(menu_bar, tearoff=False)
edit_menu.add_command(label='Undo',accelerator='Ctrl+Z', compound=tk.LEFT)
edit_menu.add_command(label='Cut',accelerator='Ctrl+X', compound=tk.LEFT,
                     command=lambda :text_editor.event_generate('<Control x>'))
edit_menu.add_command(label='Copy',accelerator='Ctrl+C', compound=tk.LEFT,
                     command=lambda :text_editor.event_generate('<Control c>'))
edit_menu.add_command(label='Paste',accelerator='Ctrl+V', compound=tk.LEFT,
                     command=lambda :text_editor.event_generate('<Control v>'))
edit_menu.add_command(label='Clear',accelerator='Ctrl+Alt+X', compound=tk.LEFT,
                     command=lambda :text_editor.delete(0.0, tk.END))
edit_menu.add_command(label='Find',accelerator='Ctrl+F', compound=tk.LEFT, command=find)
# edit_menu.add_command(label='Time/Date',accelerator='Ctrl+D', compound=ttk.LEFT,command=date_time)
menu_bar.add_cascade(label='Edit',menu=edit_menu)

#themes menu section
themes_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Themes', menu=themes_menu)
theme_choice = tk.StringVar()
themes_menu.add_radiobutton(label='Light Default', variable=theme_choice,compound=tk.LEFT
                           ,command=lambda :change_theme('white','black'))
# themes_menu.add_radiobutton(label='Dark', variable=theme_choice,compound=tk.LEFT
#                            ,command=lambda :change_theme('gray20','white'))
# themes_menu.add_radiobutton(label='Pink', variable=theme_choice,compound=tk.LEFT
#                            ,command=lambda :change_theme('pink','blue'))
# themes_menu.add_radiobutton(label='Monokai', variable=theme_choice,compound=tk.LEFT
#                            ,command=lambda :change_theme('orange','white'))
themes_menu.add_radiobutton(label='Dark', variable=theme_choice,compound=tk.LEFT
                           ,command=lambda :change_theme('#a6ece0','#544b3d'))
themes_menu.add_radiobutton(label='Pink', variable=theme_choice,compound=tk.LEFT
                           ,command=lambda :change_theme('pink','blue'))
themes_menu.add_radiobutton(label='Monokai', variable=theme_choice,compound=tk.LEFT
                           ,command=lambda :change_theme('orange','white'))


root.bind_all("<Control-s>", save_file)
root.bind_all("<Control-q>", exit_editor)
root.bind_all("<Control-o>", open_file)
root.bind_all("<Control-u>", delete_line)
root.bind_all("<Control-w>", delete_word)
root.bind_all("<Control-n>",new_file)
root.bind_all("Control-f", find)

root.bind_all("<Home>", move_cursor)  # Перемещение в начало строки
root.bind_all("<End>", move_cursor)  # Перемещение в конец строки

root.config(menu=menu_bar)
root.mainloop()
