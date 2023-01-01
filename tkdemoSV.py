# tkdemoSV.py
# tkinter GUI with Sun Valley ttk theme by rdbende
#   There may be some color rendering problems depending
#   on your system theme (filedialog in "dark" mode)
# https://github.com/rdbende/Sun-Valley-ttk-theme

from tkinter import *
from tkinter.ttk import *  # defaults all widgets as ttk
import sv_ttk
#from tkinter.ttk import Combobox, Separator
from tkinter import messagebox
from tkinter.messagebox import showerror
from tkinter import filedialog
from tkinter.font import Font
import os


class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):

        '''
        BUTTONS
        '''
        # relief styles: SUNKEN, RAISED (Default), and FLAT
        btn1 = Button(self, text="Close", command=self.done)
        btn1.grid(row=0,column=0, padx=4)

        btn2 = Button(self, text="Child Window", command=self.create_window)
        btn2.grid(row=0,column=1, padx=4)

        btn3 = Button(self, text="See Messagebox", command=self.msgbox)
        btn3.grid(row=0,column=3, padx=4)

        self.rowconfigure(0, pad=5)


        '''
        LABELFRAME and COMBOBOX (ttk) in PANEDWINDOW
        '''
        pwin = PanedWindow(self, orient=HORIZONTAL)
        pwin.grid(row=1, column=0)
        pwin.grid(columnspan=2)

        leftFrame = LabelFrame(pwin, text="Left pane",
            width=150, height=200)
        pwin.add(leftFrame)
        lbl = Label(leftFrame, text="Panedwindow\nwith\nCombobox\nttk",
            anchor=E)
        lbl.grid(row=0, column=0, sticky=W)

        self.cvar = StringVar()

        rightFrame = LabelFrame(pwin, text="Right pane", width=150)
        pwin.add(rightFrame)
        combo = Combobox(rightFrame, textvariable=self.cvar)
        combo['values'] = ('Combo OpenBSD', 'Combo NetBSD', 'Combo FreeBSD')
        combo.bind("<<ComboboxSelected>>", self.onComboSelect)
        combo.current(0)
        combo.grid(row=0, column=0, sticky='NSEW')


        '''
        OPTIONLIST
        '''
        optionlist = ('GNOME', 'Xfce', 'MATE', 'LXDE', 'KDE', 'Windows 10')
        self.v = StringVar()
        self.v.set(optionlist[1])
        optlst = OptionMenu(self, self.v, *optionlist)
        optlst.grid(row=2,column=0)


        '''
        ENTRY
        '''
        self.x = StringVar()
        entry = Entry(self, textvariable=self.x)
        entry.grid(row=2, column=1)
        self.x.set("Entry widget")
        entry.select_range(0, END)
        entry.focus()


        '''
        RADIO
        '''
        self.radval = StringVar()
        radio1 = Radiobutton(self, variable=self.radval, value='ON', text='On')
        radio2 = Radiobutton(self, variable=self.radval, value='OFF', text='Off')
        radio1.grid(row=3,column=0, sticky=S)  # sticky here keeps closer together
        radio2.grid(row=4,column=0, sticky=N)
        self.radval.set('ON')


        '''
        SPINBOX
        '''
        self.s = StringVar()
        spin = Spinbox(self, from_=1, to=9, width=6, textvariable=self.s)
        spin.grid(row=5, column=0)


        '''
        TEXT (with wrap, font, tabs, and scrollbar)
        '''
        self.tex = Text(self, relief=SUNKEN, height=6, width=30)
        self.tex.grid(column=1, row=3, rowspan=3)
        efont = Font(family='Monospace', size=11)
        self.tex.config(wrap=NONE, padx=5,
          undo=True,
          tabs=(efont.measure('  '),)
        )
        self.scrollY = Scrollbar(self, orient=VERTICAL, command=self.tex.yview)
        self.scrollY.grid(row=3, column=2, rowspan=3, sticky=N+S+W)
        self.tex['yscrollcommand'] = self.scrollY.set

        self.tex.delete("1.0", END)
        self.tex.insert(END, 'Text widget')
        #  content = self.tex.get("1.0", END)  # to get all Text contents


        '''
        CHECKBUTTONS
        '''
        Fr = Frame(self)  # one Frame with two Checkbutton
        Fr.grid(row=6, column=0)

        self.c1 = IntVar()
        chkb1 = Checkbutton(Fr, variable=self.c1, text='Over 18', width=8)
        chkb1.grid(row=0, column=0)
        self.c2 = IntVar()
        chkb2 = Checkbutton(Fr, variable=self.c2, text='Veteran', width=8)
        chkb2.grid(row=1, column=0)


        '''
        Scrolling Listbox
        '''
        self.listbox = Listbox(self, height=7)
        self.listbox.grid(row=1, column=3, pady=4)

        self.scrollbar = Scrollbar(self,orient=VERTICAL, command=self.listbox.yview)
        self.scrollbar.grid(row=1, column=4, sticky=W+N+S, pady=4)
        self.listbox['yscrollcommand'] = self.scrollbar.set
        self.listbox.bind("<<ListboxSelect>>", self.list_clicked)
        for i in range(100):
          self.listbox.insert(i, "List Item " + str(i))


        '''
        FILE DIALOGS
        '''
        openfiles = Button(self, text="OpenFiles",
                           command=self.openfile)
        openfiles.grid(column=3, row=2)
        openfiles2 = Button(self, text="OpenFiles2", command = self.openfile2)
        openfiles2.grid(column=3, row=3)
        openfiles3 = Button(self, text="Ask Directory", command = self.openfile3)
        openfiles3.grid(column=3, row=4)
        savefile = Button(self, text="Save File", command = self.savefiledlg)
        savefile.grid(column=3, row=5)
        themetog = Button(self, text="Theme",
                          command=self.toggle_theme)
        themetog.grid(column=3, row=6)

        '''
        STATUSBAR (ttk Separator)
        '''
        sep = Separator(self, orient=HORIZONTAL)
        sep.grid(row=7, column=0, columnspan=6, sticky='WE')
        statusbar = Label(self, text="This could be a statusbar ...", anchor=W)
        statusbar.grid(row=8, column=0, columnspan=6, sticky='WE')
        # Instead of a Label could use a Frame and populate it with
        # more widgets


    '''
    Functions and Handlers
    '''
    def toggle_theme(self):
        if sv_ttk.get_theme() == "dark":
            print("Setting theme to light")
            sv_ttk.use_light_theme()
        elif sv_ttk.get_theme() == "light":
            print("Setting theme to dark")
            sv_ttk.use_dark_theme()
        else:
            print("Not Sun Valley theme")

    # Add a file dialog (file and directory chooser)
    def openfile(self):
        '''
        askopenfilenames can return multiple file names
        '''
        f = filedialog.askopenfilenames(initialdir="/")
        print(f)  # f is a list

    # Specify file types (filter file extensions)
    def openfile2(self):
        f = filedialog.askopenfilename(filetypes = (("Text files","*.txt"),("all files","*.*")))
        if f:
            print(f)
            with open(f) as r:
                content = r.read()
            self.tex.delete("1.0", END)  # clear the Text widget
            self.tex.insert(END, content)  # insert the text

    # ask for a directory
    def openfile3(self):
        d = filedialog.askdirectory()
        print(d)

    # SaveAs file dialog
    def savefiledlg(self):
        print(os.path.abspath(__file__))  # fullpath with filename of current script
        print(os.path.basename(__file__)) # just the script filename
        print(os.path.dirname(os.path.abspath(__file__)))  # just the full directory path
        fname = filedialog.asksaveasfilename(confirmoverwrite=True,
            initialdir=os.path.dirname(os.path.abspath(__file__)))
        if fname:
            try:
                with open(fname, "w") as f:
                    f.write(self.tex.get("1.0", END))  # contents of the demo Text widget
            except:
                showerror("Save File", "Failed to save file\n'%s'" % fname)
            return


    '''
    MESSAGEBOX
    '''
    def msgbox(self):
        '''
        Create a MessageBox
        messagebox.showinfo('Message title', 'Message content')
        messagebox.askquestion('Message title', 'Message content') # yes no
        messagebox.askyesnocancel('Message title', 'Message content')
        messagebox.askokcancel('Message title', 'Message content')
        messagebox.askretrycancel('Message title', 'Message content')
            ok, yes, retry returns TRUE
            no, cancel returns FALSE
        '''
        messagebox.askyesno('Message title', 'askyesno example')


    counter = 0

    def create_window(self):
        self.counter += 1
        t = Toplevel(self)
        t.wm_title("Window #%s" % self.counter)
        t.geometry("300x300") # WxH+left+top
        l = Label(t, text="This is window #%s" % self.counter)
        l.grid(row=0, column=0, padx=100, pady=140)
        btn = Button(t, text="Exit", command=t.destroy)
        btn.grid(row=0, column=0, sticky=S+E, padx=25)


    def list_clicked(self, event):
        list_item = self.listbox.curselection()
        fp = self.listbox.get(list_item[0])
        print(str(fp) + " --> " + str(list_item[0]) +
            " of " + str(self.listbox.size()))


    def onComboSelect(self, e):
        '''
        generates: IndexError: tuple index out of range
        do not now why :(
        '''
        w = e.widget
        print(w.get())


    def done(self):
        print(self.v.get())  # optionlist
        print(self.x.get())  # entry field
        print(self.radval.get())  # radio button
        print(self.s.get())  # spinbox value
        print(self.tex.get(1.0, END))  # text value
        print(self.c1.get())  # checkbutton 1
        print(self.c2.get())  # checkbutton 2
        exit()


    '''
    MENUS
    '''
    def create_menu(self):
        menubar = Menu(root)
        mn_file = Menu(menubar, tearoff=0)
        mn_file.add_command(label="New", command=self.mn_file_new,
            accelerator="Ctrl-n", underline=1)
        mn_file.add_command(label="Open", command=self.nm_file_open)
        mn_file.add_command(label="Save", command=self.nm_file_save,
            accelerator="Ctrl-s", underline=1)
        mn_file.add_command(label="Save-As", command=self.nm_file_saveas)
        mn_file.add_separator()
        mn_file.add_command(label="Exit", command=self.nm_file_exit,
            accelerator="Ctrl-q")
        menubar.add_cascade(label="File", menu=mn_file)
        mn_edit = Menu(menubar, tearoff=0)
        mn_edit.add_command(label="Undo", command=self.mn_edit_undo,
            accelerator="Ctrl-z")
        mn_edit.add_command(label="Select All", command=self.mn_edit_selall,
            accelerator="Ctrl-a")
        submenu = Menu(mn_edit, tearoff=False)
        submenu.add_command(label="Copy", command=self.mn_edit_copy,
            accelerator="Ctrl-c")
        submenu.add_command(label="Paste", command=self.mn_edit_paste,
            accelerator="Ctrl-v")
        mn_edit.add_cascade(label="Clipboard", menu=submenu, underline=3)
        menubar.add_cascade(label="Edit", menu=mn_edit)
        mn_help = Menu(menubar, tearoff=0)
        mn_help.add_command(label="Help Index", command=self.mn_help_index)
        mn_help.add_command(label="See the code", command=self.mn_help_code)
        mn_help.add_command(label="About…", command=self.mn_help_about)
        menubar.add_cascade(label="Help", menu=mn_help)
        root.config(menu=menubar) # display the menu

    def mn_file_new(self):
        pass
    def nm_file_open(self):
        pass
    def nm_file_save(self):
        pass
    def nm_file_saveas(self):
        pass
    def nm_file_exit(self):
        quit()
    def mn_edit_undo(self):
        pass
    def mn_edit_selall(self):
        pass
    def mn_help_index(self):
        pass
    def mn_help_code(self):
        pass
    def mn_help_about(self):
        pass
    def eventHandler(self):
        pass
    def mn_edit_copy(self):
        pass
    def mn_edit_paste(self):
        pass

#
root = Tk()
root.geometry("565x395") # WxH+left+top
root.title("Tkinter Demo sv_ttk")
# root.overrideredirect(True) # removed window decorations
root.resizable(0,0) # no resize & removes maximize button
root.iconphoto(False, PhotoImage(file='icon.png'))
# root.attributes("-topmost", True)  # Keep on top of other windows
app = Application(master=root)
sv_ttk.set_theme("dark")
app.mainloop()
