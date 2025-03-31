import os
from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from tkinter import font
from tkinter import colorchooser

open_status_name = False
selected = ""
file_name = ""

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll

    myappid = "mycompany.myproduct.subproduct.version"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


# To open a new file
def newfile():
    text_field.delete(1.0, END)
    root.title("New File - e:Editor")


# To open a file
def open_files():
    global file_name
    text_field.delete(1.0, END)

    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Documents', '*.txt'),
             ('HTML Files', '*.html')]
    text_file = askopenfilename(initialdir=r'C:\Users\Leon\pythonProject\tkinter', title='Open File', filetypes=files)
    name = text_file
    file_name = name
    basename = os.path.basename(name)
    root.title(f'{basename} - ET-Editor')

    # Check to see if there is a file name
    if text_file:
        # Make filename global so we can access it later
        global open_status_name
        open_status_name = text_file

    text_file = open(text_file, 'r')
    content = text_file.read()
    text_field.insert(END, content)

    text_file.close()


def save_as_file():
    global file_name
    files = [('Text Documents', '*.txt'),
             ('Python Files', '*.py'),
             ('All Files', '*.*'),
             ('HTML Files', '*.html')]
    text_file = asksaveasfilename(defaultextension='.*',
                                  initialdir=r'C:\Users\Leon\PycharmProjects\pythonProject\tkinter', title='Save File',
                                  filetypes=files)
    if text_file:
        name = text_file
        name = os.path.basename(name)
        file_name = name
        root.title(f'{name} - ET-Editor')
        text_file = open(text_file, 'w')
        text_file.write(text_field.get(1.0, END))
        text_file.close()


# To save a file
def save_files():
    files = [('All Files', '*.*'),
             ('Python Files', '*.py'),
             ('Text Documents', '*.txt'),
             ('HTML Files', '*.html')]
    global open_status_name
    global file_name
    if open_status_name:
        save_file = asksaveasfilename(defaultextension='.txt',
                                      initialdir=file_name,
                                      title='Save File',
                                      filetypes=files)
        name = save_file
        basename = os.path.basename(name)
        root.title(f'{basename} - ET-Editor')
        save_file = open(save_file, 'w')
        save_file.write(text_field.get(1.0, END))
        save_file.close()
    else:
        save_as_file()


# To select all text in the text widget
def select_all():
    text_field.tag_add('sel', 1.0, END)


# Creating cut function
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if text_field.selection_get():
            selected = text_field.selection_get()
            text_field.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)


# Creating copy function
def copy_text(e):
    global selected

    if e:
        selected = root.clipboard_get()

    if text_field.selection_get():
        selected = text_field.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)


# Creating paste function
def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = text_field.index(INSERT)
            text_field.insert(position, selected)


# To quit the program
def quit_text_editor():
    root.destroy()


# Bold text
def bold_it():
    bold_font = font.Font(text_field, text_field.cget("font"))
    bold_font.configure(weight="bold")

    text_field.tag_configure("bold", font=bold_font)

    current_tags = text_field.tag_names("sel.first")

    if "bold" in current_tags:
        text_field.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_field.tag_add("bold", "sel.first", "sel.last")


# Italics text
def italics_it():
    italic_font = font.Font(text_field, text_field.cget("font"))
    italic_font.configure(slant="italic")

    text_field.tag_configure("italic", font=italic_font)

    current_tags = text_field.tag_names("sel.first")

    if "italic" in current_tags:
        text_field.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_field.tag_add("italic", "sel.first", "sel.last")


# Function to change text colour
def text_colour():
    # Choosing a colour
    my_colour = colorchooser.askcolor()[1]
    if my_colour:
        colour_font = font.Font(text_field, text_field.cget("font"))

        text_field.tag_configure("coloured", font=colour_font, foreground=my_colour)

        current_tags = text_field.tag_names("sel.first")

        if "coloured" in current_tags:
            text_field.tag_remove("coloured", "sel.first", "sel.last")
        else:
            text_field.tag_add("coloured", "sel.first", "sel.last")


# Change background colour
def bg_colour():
    my_colour = colorchooser.askcolor()[1]
    if my_colour:
        text_field.config(bg=my_colour)


# Change all text colour
def all_text_colour():
    my_colour = colorchooser.askcolor()[1]
    if my_colour:
        text_field.config(fg=my_colour)


# Creating main window
root = Tk()
root.state('zoomed')
root.geometry("500x500")
root.title("Untitled - ET-Editor")

icon = PhotoImage(file='note-taking.png')
root.iconphoto(False, icon)
root.iconbitmap('note-taking.ico')

# Creating Main Frame for window
frame = ttk.Frame(root)

# Creating toolbar frame
toolbar_frame = Frame(root)

# Packing both frames
toolbar_frame.pack(fill=X)
frame.pack()

# Creating a scrollbar for the text widget
text_scroll = ttk.Scrollbar(frame)
text_scroll.pack(side=RIGHT, fill=Y)

# Creating text widget
text_field = Text(frame, width=126, height=30, font=('Sabon', 16), undo=True, wrap=WORD,
                  yscrollcommand=text_scroll.set)
text_field.pack()

# Configuring scrollbar
text_scroll.config(command=text_field.yview)

# Creating menubar
menubar = Menu(root)
root.config(menu=menubar)

# File menu
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="New File", command=lambda: newfile(), accelerator='Ctrl+N')
file.add_command(label="Open..", command=lambda: open_files(), accelerator='Ctrl+O')
file.add_command(label="Save", command=lambda: save_files(), accelerator='Ctrl+S')
file.add_command(label="Save As", command=lambda: save_as_file(), accelerator='Ctrl+E')
file.add_separator()
file.add_command(label="Quit", command=quit_text_editor, accelerator='Ctrl+w')

# Edit menu
edit = Menu(root, tearoff=0)
menubar.add_cascade(label="Edit", menu=edit)
edit.add_command(label="Select All", command=lambda: select_all(), accelerator='Ctrl+A')
edit.add_command(label="Cut", command=lambda: cut_text(False), accelerator='Ctrl+X')
edit.add_command(label="Copy", command=lambda: copy_text(False), accelerator='Ctrl+C')
edit.add_command(label="Paste", command=lambda: paste_text(False), accelerator='Ctrl+V')
edit.add_command(label="Undo", command=text_field.edit_undo, accelerator='Ctrl+Z')
edit.add_command(label="Redo", command=text_field.edit_redo, accelerator='Ctrl+Y')

# Colour Menu
colour = Menu(root, tearoff=0)
menubar.add_cascade(label="Colours", menu=colour)
colour.add_command(label="Selected text", command=text_colour)
colour.add_command(label="All Text", command=all_text_colour)
colour.add_command(label="Background", command=bg_colour)

# Creating buttons
bold_btn = ttk.Button(toolbar_frame, text='Bold \t(Ctrl+B)', command=lambda: bold_it())
bold_btn.grid(row=0, column=0, sticky=W, padx=2)

italics_btn = ttk.Button(toolbar_frame, text='Italics \t(Ctrl+L)', command=lambda: italics_it())
italics_btn.grid(row=0, column=1, padx=2)

colour_text_btn = ttk.Button(toolbar_frame, text='Text Colour \t(Ctrl+k)', command=lambda: text_colour())
colour_text_btn.grid(row=0, column=3, padx=2)

# Binding menu options to shortcuts
root.bind('<Control-n>', lambda event: newfile())
root.bind('<Control-o>', lambda event: open_files())
root.bind('<Control-s>', lambda event: save_files())
root.bind('<Control-w>', lambda event: quit_text_editor())
root.bind('<Control-a>', lambda event: select_all())
root.bind('<Control-e>', lambda event: save_as_file())
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)
root.bind('<Control-k>', lambda event: text_colour())

root.bind('<Control-b>', lambda event: bold_it())
root.bind('<Control-l>', lambda event: italics_it())

root.mainloop()
