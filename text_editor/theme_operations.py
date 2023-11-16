class ThemeOperations:
    def __init__(self, text_editor):
        self.text_editor = text_editor

    def change_theme(self, bg_color, fg_color):
        self.text_editor.text_editor.config(bg=bg_color, fg=fg_color)
