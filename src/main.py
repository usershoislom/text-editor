from editor import TextEditor
from file_operations import FileOperations
from find_replace import FindReplace
from theme_operations import ThemeOperations

def main():
    text_editor = TextEditor()
    file_operations = FileOperations(text_editor)
    find_replace = FindReplace(text_editor)
    theme_operations = ThemeOperations(text_editor)

    text_editor.file_operations = file_operations
    text_editor.find_replace = find_replace
    text_editor.theme_operations = theme_operations

    text_editor.run()

main()
