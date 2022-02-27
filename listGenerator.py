from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import os
import webbrowser


switchReturn = ''
firstLoad = True
entryBoxReturn = ''
buttonSubmitted = False


class entryDialog :
    def __init__(self, parent, message, default=None, justNumbers=False):
        """

        :param parent: Root Tk() window
        :param message: Help Message
        :param default: (Optional) Default entry text
        :param justNumbers: (Optional) If true, dialog only accepts numbers

        """

        global entryBoxReturn
        self.numList = ['1','2','3','4','5','6','7','8','9','0']
        self.keyList = ['BackSpace', 'Delete', 'KP_0', 'KP_1', 'KP_2', 'KP_3', 'KP_4', 'KP_5', 'KP_6', 'KP_7', 'KP_8', 'KP_9']
        self.parent = parent
        self.top = Toplevel(self.parent)
        self.isSubmit = False
        self.top.geometry("253x175+655+162")
        self.top.title("Question")
        self.top.configure(background="#d9d9d9")
        self.top.resizable(0, 0)
        self.top.grab_set()

        self.theMessage = Message(self.top)
        self.theMessage.place(relx=0.04, rely=0.11, relheight=0.13, relwidth=0.91)
        self.theMessage.configure(foreground="#000000")
        self.theMessage.configure(highlightbackground="#d9d9d9")
        self.theMessage.configure(background='#d9d9d9')
        self.theMessage.configure(highlightcolor="black")
        self.theMessage.configure(text=str(message))
        self.theMessage.configure(width=230)

        self.entryText = StringVar()

        self.entryBox = Entry(self.top)
        self.entryBox.place(relx=0.16, rely=0.34, relheight=0.11, relwidth=0.69)
        self.entryBox.configure(background="white")
        self.entryBox.configure(disabledforeground="#a3a3a3")
        self.entryBox.configure(font="TkFixedFont")
        self.entryBox.configure(foreground="#000000")
        self.entryBox.configure(insertbackground="black")
        self.entryBox.configure(width=174)
        self.entryBox.configure(textvar=self.entryText)
        self.entryBox.bind('<Return>', lambda x : self.setVars())
        if justNumbers :
            self.entryBox.bind('<KeyPress>', self.validateKeys)
        if default != None :
            self.entryText.set(str(default))

        self.sendButton = Button(self.top)
        self.sendButton.place(relx=0.36, rely=0.69, height=24, width=67)
        self.sendButton.configure(activebackground="#d9d9d9")
        self.sendButton.configure(activeforeground="#000000")
        self.sendButton.configure(disabledforeground="#a3a3a3")
        self.sendButton.configure(foreground="#000000")
        self.sendButton.configure(highlightbackground="#d9d9d9")
        self.sendButton.configure(highlightcolor="black")
        self.sendButton.configure(pady="0")
        self.sendButton.configure(text='''Submit''')
        self.sendButton.configure(width=67)
        self.sendButton.configure(command=self.setVars)

        self.entryBox.focus_set()

    def setVars(self):
        global buttonSubmitted
        global entryBoxReturn
        if self.entryBox.get().strip() == '' :
            return False
        entryBoxReturn = str(self.entryBox.get().strip())
        self.isSubmit = True
        buttonSubmitted = True
        self.top.destroy()

    def validateKeys(self, press):
        if press.char in self.numList :
            return True
        elif press.keysym in self.keyList :
            return True
        else :
            return 'break'


class Question:
    def __init__(self, parent, groups, message) :
        """

        :param parent: Root Tk() window
        :param groups: Dictionary containing groups for list population
        :param message: Help Message

        """

        _bgcolor = '#d9d9d9'

        self.groups = groups
        self.parent = parent
        self.top = Toplevel(self.parent)

        self.top.geometry("435x362+544+76")
        self.top.resizable(0,0)
        self.top.title("Question")
        self.top.configure(background="#d9d9d9")

        self.top.grab_set()

        self.statusString = StringVar()
        self.statusString.set('')
        self.toRename = {}

        self.groupsList = Listbox(self.top)
        self.groupsList.place(relx=0.16, rely=0.11, relheight=0.67, relwidth=0.7)
        self.groupsList.configure(background="white")
        self.groupsList.configure(disabledforeground="#a3a3a3")
        self.groupsList.configure(font="TkFixedFont")
        self.groupsList.configure(foreground="#000000")
        self.groupsList.configure(width=304)
        self.groupsList.bind('<<ListboxSelect>>', lambda x : self.quickView())
        self.groupsList.bind('<Return>', lambda x : self.submit())
        self.groupsList.bind('<Double-1>', lambda x : self.submit())
        self.groupsList.bind('<Button-3>', self.popup)

        self.quickScroll = Scrollbar(self.groupsList, orient=VERTICAL)
        self.quickScroll.place(relx=0.60, rely=0.004, relheight=1, relwidth=0.41)

        self.groupsList.config(yscrollcommand=self.quickScroll.set)
        self.quickScroll.config(command=self.groupsList.yview)


        self.groupHelp = Message(self.top)
        self.groupHelp.place(relx=-0.25, rely=0.0, relheight=0.09, relwidth=1.5)
        self.groupHelp.configure(background=_bgcolor)
        self.groupHelp.configure(foreground="#000000")
        self.groupHelp.configure(highlightbackground="#d9d9d9")
        self.groupHelp.configure(highlightcolor="black")
        self.groupHelp.configure(text=str(message))
        self.groupHelp.configure(width=430)

        self.moveButton = Button(self.top)
        self.moveButton.place(relx=0.41, rely=0.91, height=24, width=77)
        self.moveButton.configure(activebackground="#d9d9d9")
        self.moveButton.configure(activeforeground="#000000")
        self.moveButton.configure(background=_bgcolor)
        self.moveButton.configure(disabledforeground="#a3a3a3")
        self.moveButton.configure(foreground="#000000")
        self.moveButton.configure(highlightbackground="#d9d9d9")
        self.moveButton.configure(highlightcolor="black")
        self.moveButton.configure(pady="0")
        self.moveButton.configure(text='''Move''')
        self.moveButton.configure(width=67)
        self.moveButton.configure(command=self.submit)

        self.isSubmit = False

        self.status = Label(self.top)
        self.status.place(relx=0.0, rely=0.80, height=31, width=434)
        self.status.configure(background=_bgcolor)
        self.status.configure(disabledforeground="#a3a3a3")
        self.status.configure(foreground="#000000")
        self.status.configure(textvar=self.statusString)
        self.status.configure(width=434)

        self.groupMenu = Menu(self.top, tearoff=0)
        self.groupMenu.add_command(label='Add Group', command=lambda : self.editGroup(op='add'))
        self.groupMenu.add_command(label='Remove Group', command=lambda : self.editGroup(op='remove'))
        self.groupMenu.add_separator()
        self.groupMenu.add_command(label='Rename Group', command=self.rename)

        self.editMenu = Menu(self.top, tearoff=0)
        self.editMenu.add_command(label='Add Group', command=lambda: self.editGroup(op='add'))

        for group in sorted(self.groups.keys()) :
            self.groupsList.insert(END, str(group))

    def reloadGroups(self):
        try :
            self.groupsList.delete(0, END)
            for group in sorted(self.groups.keys()) :
                self.groupsList.insert(END, str(group))
        except :
            pass

    def editGroup(self, op):
        global entryBoxReturn
        if op == 'add' :
            self.entry = entryDialog(message='Please type in the name of the new group:', parent=self.parent)
            self.entry.parent.wait_window(self.entry.top)
            if self.entry.isSubmit :
                if entryBoxReturn not in list(self.groups.keys()) :
                    self.groups[entryBoxReturn] = []
                    self.reloadGroups()
                else :
                    messagebox.showerror('Oops!', 'A group already has that name!')
            else :
                pass
        elif op == 'remove' :
            if messagebox.askokcancel('Are you sure about that?', 'Deleting the selected group will also delete all of it\'s content!') :
                del self.groups[self.groupsList.get(self.groupsList.curselection())]
                self.reloadGroups()

    def popup(self, event):
        if self.groupsList.curselection() != () :
            self.groupMenu.tk_popup(x=event.x_root+1, y=event.y_root+2)
        else :
            self.editMenu.tk_popup(x=event.x_root+1, y=event.y_root+2)

    def quickView(self):
        self.selected = self.groupsList.get(self.groupsList.curselection())
        self.quickString = self.selected + ' contains: '
        self.quickString += ', '.join(self.groups[self.selected])
        if len(self.quickString) > 85 :
            self.shortString = str(self.quickString[:80])
            self.shortQuickString = self.shortString + '...'
            self.statusString.set(self.shortQuickString)
        else :
            self.statusString.set(self.quickString)

    def rename(self):
        global entryBoxReturn
        self.selectionIndex = self.groupsList.curselection()
        self.question = entryDialog(self.parent, 'Please type in the new name of ' + str(self.groupsList.get(self.groupsList.curselection())) + ' :', str(self.groupsList.get(self.groupsList.curselection())),justNumbers=False)
        self.question.parent.wait_window(self.question.top)
        if self.question.isSubmit :
            self.groups[str(entryBoxReturn)] = self.groups.pop(str(self.groupsList.get(self.selectionIndex)))
            self.groupsList.delete(self.selectionIndex)
            self.groupsList.insert(self.selectionIndex, str(entryBoxReturn))

    def submit(self):
        global switchReturn
        if self.groupsList.curselection() != () :
            self.isSubmit = True
            switchReturn = str(self.groupsList.get(self.groupsList.curselection()))
            self.top.destroy()
        else :
            messagebox.showwarning('Oops!', 'You didn\'t select anything!', parent=self.top)


class listGen(Frame) :
    def __init__(self, parent):
        """

        :param parent: Root Tk() window

        """

        self._bgcolor = '#d9d9d9'
        self.parent = parent
        self.parent.resizable(0, 0)
        super().__init__()
        try :
            self.parent.iconphoto(True, PhotoImage(file=os.getcwd() + '\edit-512.png'))
        except :
            pass

        self.mode = 'startup'

        self.entryValue = StringVar()
        self.parent.title("List Editor")
        self.parent.withdraw()
        self.listTop = Toplevel(self.parent)
        self.listTop.title("List Editor")
        self.listTop.configure(background="#d9d9d9")
        self.listTop.configure(highlightbackground="#d9d9d9")
        self.listTop.configure(highlightcolor="black")
        self.listTop.geometry("578x124+650+150")
        self.listTop.protocol('WM_DELETE_WINDOW', sys.exit)

        self.makeNew = Button(self.listTop)
        self.makeNew.place(relx=0.03, rely=0.32, height=44, width=210)
        self.makeNew.configure(activebackground="#d9d9d9")
        self.makeNew.configure(activeforeground="#000000")
        self.makeNew.configure(background=self._bgcolor)
        self.makeNew.configure(disabledforeground="#a3a3a3")
        self.makeNew.configure(foreground="#000000")
        self.makeNew.configure(highlightbackground="#d9d9d9")
        self.makeNew.configure(highlightcolor="black")
        self.makeNew.configure(pady="0")
        self.makeNew.configure(text='''Create New List''')
        self.makeNew.configure(width=210)
        self.makeNew.configure(command=lambda : self.drawWidgets(group=False))

        self.findOld = Button(self.listTop)
        self.findOld.place(relx=0.61, rely=0.32, height=44, width=210)
        self.findOld.configure(activebackground="#d9d9d9")
        self.findOld.configure(activeforeground="#000000")
        self.findOld.configure(background=self._bgcolor)
        self.findOld.configure(disabledforeground="#a3a3a3")
        self.findOld.configure(foreground="#000000")
        self.findOld.configure(highlightbackground="#d9d9d9")
        self.findOld.configure(highlightcolor="black")
        self.findOld.configure(pady="0")
        self.findOld.configure(text='''Browse For List/Group''')
        self.findOld.configure(width=210)
        self.findOld.configure(command=self.loadBox)
        self.statusVar = StringVar()

        self.theMenu = Menu(self.listTop, bg=self._bgcolor)
        self.listTop.configure(menu=self.theMenu)

        self.aboutMenu = Menu(self.listTop, tearoff=0)
        self.theMenu.add_cascade(menu=self.aboutMenu, activebackground="#d9d9d9", activeforeground="#111111", background="#d9d9d9", foreground="#000000", label="Info")
        self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9", command=lambda: self.about('about'), foreground="#000000", label="About")
        self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9", command=lambda: self.about('github'), foreground="#000000", label="GitHub")

        self.help = Menu(self.listTop, tearoff=0)
        self.theMenu.add_cascade(menu=self.help, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Help")
        self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9", command=lambda: messagebox.showinfo('Create New List', 'If you want to create a new list file for use in RandomPicker, click this button to create a new list.'), foreground="#000000", label="Create New List")
        self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9", command=lambda: messagebox.showinfo('Browse for List/Group', 'If you already have a list/group file you want to edit, click this button to browse for the file and open it.'), foreground="#000000", label="Browse for List/Group")

    def drawWidgets(self, group) :
        if group :
            self.listTop.destroy()
            self.listTop = Toplevel(self.parent)
            self.listTop.title("List Editor")
            self.listTop.configure(background="#d9d9d9")
            self.listTop.configure(highlightbackground="#d9d9d9")
            self.listTop.configure(highlightcolor="black")
            self.listTop.geometry("618x450+716+174")
            self.listTop.resizable(0,0)
            self.listTop.protocol('WM_DELETE_WINDOW', sys.exit)
            self.textEntry = Entry(self.listTop)
            self.textEntry.place(relx=0.12, rely=0.16, relheight=0.04, relwidth=0.31)

            self.mode = 'group'

            self.textEntry.configure(background="white")
            self.textEntry.configure(disabledforeground="#a3a3a3")
            self.textEntry.configure(font="TkFixedFont")
            self.textEntry.configure(foreground="#000000")
            self.textEntry.configure(highlightbackground="#d9d9d9")
            self.textEntry.configure(highlightcolor="black")
            self.textEntry.configure(insertbackground="black")
            self.textEntry.configure(selectbackground="#c4c4c4")
            self.textEntry.configure(selectforeground="black")
            self.textEntry.configure(textvar=self.entryValue)
            self.textEntry.bind('<Return>', lambda x: self.editBox(1, self.entryValue.get(), group=True))

            self.addButton = Button(self.listTop)
            self.addButton.place(relx=0.08, rely=0.28, height=34, width=77)
            self.addButton.configure(activebackground="#d9d9d9")
            self.addButton.configure(activeforeground="#000000")
            self.addButton.configure(background=self._bgcolor)
            self.addButton.configure(disabledforeground="#a3a3a3")
            self.addButton.configure(foreground="#000000")
            self.addButton.configure(highlightbackground="#d9d9d9")
            self.addButton.configure(highlightcolor="black")
            self.addButton.configure(pady="0")
            self.addButton.configure(text='''Add''')
            self.addButton.configure(command=lambda: self.editBox(1, self.entryValue.get(), group=True))

            self.deleteButton = Button(self.listTop)
            self.deleteButton.place(relx=0.35, rely=0.28, height=34, width=77)
            self.deleteButton.configure(activebackground="#d9d9d9")
            self.deleteButton.configure(activeforeground="#000000")
            self.deleteButton.configure(background=self._bgcolor)
            self.deleteButton.configure(disabledforeground="#a3a3a3")
            self.deleteButton.configure(foreground="#000000")
            self.deleteButton.configure(highlightbackground="#d9d9d9")
            self.deleteButton.configure(highlightcolor="black")
            self.deleteButton.configure(pady="0")
            self.deleteButton.configure(text='''Delete''')
            self.deleteButton.configure(command=lambda: self.editBox(2, group=True))

            self.switchButton = Button(self.listTop)
            self.switchButton.place(relx=0.112, rely=0.42, height=34, width=93)
            self.switchButton.configure(activebackground="#d9d9d9")
            self.switchButton.configure(activeforeground="#000000")
            self.switchButton.configure(background=self._bgcolor)
            self.switchButton.configure(disabledforeground="#a3a3a3")
            self.switchButton.configure(foreground="#000000")
            self.switchButton.configure(highlightbackground="#d9d9d9")
            self.switchButton.configure(highlightcolor="black")
            self.switchButton.configure(pady="0")
            self.switchButton.configure(text='''Manage Groups''')
            self.switchButton.configure(width=93)
            self.switchButton.configure(command=lambda : self.loadBox(isGroup=True, quiet=True))


            self.helpMsg = Message(self.listTop)
            self.helpMsg.place(relx=0.03, rely=0.07, relheight=0.05, relwidth=0.47)
            self.helpMsg.configure(background=self._bgcolor)
            self.helpMsg.configure(foreground="#000000")
            self.helpMsg.configure(highlightbackground="#d9d9d9")
            self.helpMsg.configure(highlightcolor="black")
            self.helpMsg.configure(text='''Please enter an option to be added to the list:''')
            self.helpMsg.configure(width=280)

            self.browseButton = Button(self.listTop)
            self.browseButton.place(relx=0.18, rely=0.70, height=34, width=117)
            self.browseButton.configure(activebackground="#d9d9d9")
            self.browseButton.configure(activeforeground="#000000")
            self.browseButton.configure(background=self._bgcolor)
            self.browseButton.configure(disabledforeground="#a3a3a3")
            self.browseButton.configure(foreground="#000000")
            self.browseButton.configure(highlightbackground="#d9d9d9")
            self.browseButton.configure(highlightcolor="black")
            self.browseButton.configure(pady="0")
            self.browseButton.configure(text='''Browse for list''')
            self.browseButton.configure(command=self.loadBox)

            self.clearButton = Button(self.listTop)
            self.clearButton.place(relx=0.18, rely=0.82, height=34, width=117)
            self.clearButton.configure(activebackground="#FF0000")
            self.clearButton.configure(activeforeground="#000000")
            self.clearButton.configure(background=self._bgcolor)
            self.clearButton.configure(disabledforeground="#a3a3a3")
            self.clearButton.configure(foreground="#FF0000")
            self.clearButton.configure(highlightbackground="#d9d9d9")
            self.clearButton.configure(highlightcolor="black")
            self.clearButton.configure(pady="0")
            self.clearButton.configure(text='''Clear list''')
            self.clearButton.configure(command=lambda: self.editBox(op=3, group=True))

            self.statusLabel = Label(self.listTop)
            self.statusLabel.place(relx=0.03, rely=0.90, height=30, width=300)
            self.statusLabel.configure(background=self._bgcolor)
            self.statusLabel.configure(disabledforeground="#a3a3a3")
            self.statusLabel.configure(foreground="#000000")
            self.statusLabel.configure(textvar=self.statusVar)
            self.statusLabel.configure(width=500)

            self.saveButton = Button(self.listTop)
            self.saveButton.place(relx=0.18, rely=0.58, height=34, width=117)
            self.saveButton.configure(activebackground="#d9d9d9")
            self.saveButton.configure(activeforeground="#000000")
            self.saveButton.configure(background=self._bgcolor)
            self.saveButton.configure(disabledforeground="#a3a3a3")
            self.saveButton.configure(foreground="#000000")
            self.saveButton.configure(highlightbackground="#d9d9d9")
            self.saveButton.configure(highlightcolor="black")
            self.saveButton.configure(pady="0")
            self.saveButton.configure(text='''Save list''')
            self.saveButton.configure(command=lambda : self.saveBox(group=True))

            self.listBox = Listbox(self.listTop)
            self.listBox.place(relx=0.57, rely=0.04, relheight=0.89, relwidth=0.41)
            self.listBox.configure(background="white")
            self.listBox.configure(disabledforeground="#a3a3a3")
            self.listBox.configure(font="TkFixedFont")
            self.listBox.configure(foreground="#000000")
            self.listBox.configure(width=10)

            self.itemMove = Button(self.listTop)
            self.itemMove.place(relx=0.3, rely=0.42, height=34, width=87)
            self.itemMove.configure(activebackground="#d9d9d9")
            self.itemMove.configure(activeforeground="#000000")
            self.itemMove.configure(background=self._bgcolor)
            self.itemMove.configure(disabledforeground="#a3a3a3")
            self.itemMove.configure(foreground="#000000")
            self.itemMove.configure(highlightbackground="#d9d9d9")
            self.itemMove.configure(highlightcolor="black")
            self.itemMove.configure(pady="0")
            self.itemMove.configure(text='''Move Item''')
            self.itemMove.configure(width=87)
            self.itemMove.configure(command=lambda: self.checkListBox())

            self.scroll = Scrollbar(self.listBox, orient=VERTICAL)
            self.scroll.place(relx=0.57, rely=0.003, relheight=1, relwidth=0.41)

            self.listBox.config(yscrollcommand=self.scroll.set)
            self.scroll.config(command=self.listBox.yview)

            self.theMenu = Menu(self.listTop, bg=self._bgcolor)
            self.listTop.configure(menu=self.theMenu)

            self.aboutMenu = Menu(self.listTop, tearoff=0)
            self.theMenu.add_cascade(menu=self.aboutMenu, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Info")
            self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.about('about'), foreground="#000000", label="About")
            self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.about('github'), foreground="#000000", label="GitHub")

            self.help = Menu(self.listTop, tearoff=0)
            self.theMenu.add_cascade(menu=self.help, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Help")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('add/delete'), foreground="#000000",label="Add/Delete Buttons")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('browse/save'), foreground="#000000",label="Browse for List / Save List")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('clear'), foreground="#000000", label="Clear List Button")

        elif not group :
            self.listTop.destroy()
            self.listTop = Toplevel(self.parent)
            self.listTop.title("List Editor")
            self.listTop.configure(background="#d9d9d9")
            self.listTop.configure(highlightbackground="#d9d9d9")
            self.listTop.configure(highlightcolor="black")
            self.listTop.resizable(0,0)
            self.listTop.geometry("618x450+716+174")
            self.listTop.protocol('WM_DELETE_WINDOW', sys.exit)

            self.mode = 'list'

            self.textEntry = Entry(self.listTop)
            self.textEntry.place(relx=0.12, rely=0.16, relheight=0.04, relwidth=0.31)

            self.textEntry.configure(background="white")
            self.textEntry.configure(disabledforeground="#a3a3a3")
            self.textEntry.configure(font="TkFixedFont")
            self.textEntry.configure(foreground="#000000")
            self.textEntry.configure(highlightbackground="#d9d9d9")
            self.textEntry.configure(highlightcolor="black")
            self.textEntry.configure(insertbackground="black")
            self.textEntry.configure(selectbackground="#c4c4c4")
            self.textEntry.configure(selectforeground="black")
            self.textEntry.configure(textvar=self.entryValue)
            self.textEntry.bind('<Return>', lambda x: self.editBox(1, self.entryValue.get()))

            self.addButton = Button(self.listTop)
            self.addButton.place(relx=0.08, rely=0.36, height=34, width=77)
            self.addButton.configure(activebackground="#d9d9d9")
            self.addButton.configure(activeforeground="#000000")
            self.addButton.configure(background=self._bgcolor)
            self.addButton.configure(disabledforeground="#a3a3a3")
            self.addButton.configure(foreground="#000000")
            self.addButton.configure(highlightbackground="#d9d9d9")
            self.addButton.configure(highlightcolor="black")
            self.addButton.configure(pady="0")
            self.addButton.configure(text='''Add''')
            self.addButton.configure(command=lambda: self.editBox(1, self.entryValue.get()))

            self.deleteButton = Button(self.listTop)
            self.deleteButton.place(relx=0.35, rely=0.36, height=34, width=77)
            self.deleteButton.configure(activebackground="#d9d9d9")
            self.deleteButton.configure(activeforeground="#000000")
            self.deleteButton.configure(background=self._bgcolor)
            self.deleteButton.configure(disabledforeground="#a3a3a3")
            self.deleteButton.configure(foreground="#000000")
            self.deleteButton.configure(highlightbackground="#d9d9d9")
            self.deleteButton.configure(highlightcolor="black")
            self.deleteButton.configure(pady="0")
            self.deleteButton.configure(text='''Delete''')
            self.deleteButton.configure(command=lambda: self.editBox(2))

            self.helpMsg = Message(self.listTop)
            self.helpMsg.place(relx=0.03, rely=0.07, relheight=0.05, relwidth=0.47)
            self.helpMsg.configure(background=self._bgcolor)
            self.helpMsg.configure(foreground="#000000")
            self.helpMsg.configure(highlightbackground="#d9d9d9")
            self.helpMsg.configure(highlightcolor="black")
            self.helpMsg.configure(text='''Please enter an option to be added to the list:''')
            self.helpMsg.configure(width=280)

            self.browseButton = Button(self.listTop)
            self.browseButton.place(relx=0.18, rely=0.70, height=34, width=117)
            self.browseButton.configure(activebackground="#d9d9d9")
            self.browseButton.configure(activeforeground="#000000")
            self.browseButton.configure(background=self._bgcolor)
            self.browseButton.configure(disabledforeground="#a3a3a3")
            self.browseButton.configure(foreground="#000000")
            self.browseButton.configure(highlightbackground="#d9d9d9")
            self.browseButton.configure(highlightcolor="black")
            self.browseButton.configure(pady="0")
            self.browseButton.configure(text='''Browse for list''')
            self.browseButton.configure(command=self.loadBox)

            self.clearButton = Button(self.listTop)
            self.clearButton.place(relx=0.18, rely=0.82, height=34, width=117)
            self.clearButton.configure(activebackground="#FF0000")
            self.clearButton.configure(activeforeground="#000000")
            self.clearButton.configure(background=self._bgcolor)
            self.clearButton.configure(disabledforeground="#a3a3a3")
            self.clearButton.configure(foreground="#FF0000")
            self.clearButton.configure(highlightbackground="#d9d9d9")
            self.clearButton.configure(highlightcolor="black")
            self.clearButton.configure(pady="0")
            self.clearButton.configure(text='''Clear list''')
            self.clearButton.configure(command=lambda: self.editBox(op=3))

            self.saveButton = Button(self.listTop)
            self.saveButton.place(relx=0.18, rely=0.58, height=34, width=117)
            self.saveButton.configure(activebackground="#d9d9d9")
            self.saveButton.configure(activeforeground="#000000")
            self.saveButton.configure(background=self._bgcolor)
            self.saveButton.configure(disabledforeground="#a3a3a3")
            self.saveButton.configure(foreground="#000000")
            self.saveButton.configure(highlightbackground="#d9d9d9")
            self.saveButton.configure(highlightcolor="black")
            self.saveButton.configure(pady="0")
            self.saveButton.configure(text='''Save list''')
            self.saveButton.configure(command=self.saveBox)

            self.listBox = Listbox(self.listTop)
            self.listBox.place(relx=0.57, rely=0.04, relheight=0.89, relwidth=0.41)
            self.listBox.configure(background="white")
            self.listBox.configure(disabledforeground="#a3a3a3")
            self.listBox.configure(font="TkFixedFont")
            self.listBox.configure(foreground="#000000")
            self.listBox.configure(width=10)

            self.scroll = Scrollbar(self.listBox, orient=VERTICAL)
            self.scroll.place(relx=0.57, rely=0.003, relheight=1, relwidth=0.41)

            self.listBox.config(yscrollcommand=self.scroll.set)
            self.scroll.config(command=self.listBox.yview)

            self.theMenu = Menu(self.listTop, bg=self._bgcolor)
            self.listTop.configure(menu=self.theMenu)

            self.aboutMenu = Menu(self.listTop, tearoff=0)
            self.theMenu.add_cascade(menu=self.aboutMenu, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Info")
            self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9", command=lambda: self.about('about'), foreground="#000000", label="About")
            self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.about('github'), foreground="#000000", label="GitHub")
            self.help = Menu(self.listTop, tearoff=0)
            self.theMenu.add_cascade(menu=self.help, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Help")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('add/delete'), foreground="#000000",label="Add/Delete Buttons")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('browse/save'), foreground="#000000",label="Browse for List /Save List")
            self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('clear'), foreground="#000000", label="Clear List Button")

    def editBox(self, op, text='', group=False) :
        global switchReturn
        if op == 1 :
            if text.strip() == '' :
                self.entryValue.set('')
                messagebox.showwarning('Oops!', 'You didn\'t type anything in!')
            else :
                if not group :
                    self.listBox.insert(END, str(text).strip())
                    self.entryValue.set('')
                else :
                    self.listBox.insert(END, str(text).strip())
                    self.groupDict[switchReturn].append(str(text).strip())
                    self.entryValue.set('')

        elif op == 2 :
            self.selectionIndex = self.listBox.curselection()
            if self.selectionIndex != () :
                if not group :
                    self.listBox.delete(self.selectionIndex)
                    self.selectionIndex = None
                else :
                    self.groupDict[switchReturn].remove(self.listBox.get(self.listBox.curselection()))
                    self.listBox.delete(self.selectionIndex)
                    self.selectionIndex = None
            else :
                messagebox.showwarning('Oops!', 'You didn\'t select anything!')

        elif op == 3 :
            if self.listBox.get(0, END) != () :
                if messagebox.askokcancel('Are you sure about that?', 'Are you sure you would like to clear the list?') == True :
                    if not group :
                        self.listBox.delete(0, END)
                        messagebox.showinfo('Done!', 'Your list has been cleared!')
                    else:
                        self.groupDict[switchReturn] = []
                        self.listBox.delete(0, END)
                        messagebox.showinfo('Done!', 'Your list has been cleared!')
                    return True
                else :
                    return False
            else :
                messagebox.showwarning('Oops!', 'You didn\'t have anything in your list!')
                return False

    def saveBox(self, group=False):
        try :
            self.file_type = [("Text files", "*.txt", "TEXT")]
            self.saveFile = filedialog.asksaveasfile(mode='w', filetypes=self.file_type, defaultextension='.txt')
            if self.saveFile != None :
                if not group :
                    self.tupList = list(self.listBox.get(0, END))
                    self.listText = ';'.join(self.tupList)
                    self.saveFile.write(self.listText)
                    self.saveFile.close()
                else :
                    try:
                        self.partList = []
                        self.file_type = [("Text files", "*.txt", "TEXT")]
                        for item in sorted(self.groupDict.keys()):
                            self.saveFile.write(';-[' + str(item) + ']-; \n \n')
                            self.partList = self.groupDict[item]
                            for part in self.partList:
                                self.saveFile.write(str(part) + '; \n')
                            self.saveFile.write('\n')
                        self.saveFile.close()
                        self.yayOrNay = messagebox.askyesno('Group File Created!', 'Would you like to open the new group file?')
                        if self.yayOrNay == True:
                            webbrowser.open(self.saveFile.name)
                    except :
                        messagebox.showerror('Ut-Oh!', 'An error occurred saving the file! Please try again!')
                        return False
            else :
                messagebox.showerror('Oops', 'You didn\'t choose a file!')
                return False
        except:
            messagebox.showerror('Ut-Oh!', 'An error occurred saving the file! Please try again!')
            return False

    def findGroups(self, group=None, move=None):
        global switchReturn, firstLoad
        self.newKey = ''
        self.needsKey = False
        if firstLoad :
            self.groupDict = {}
            for item in self.readList:
                try:
                    self.nextItem = self.readList[self.readList.index(item) + 1]
                except IndexError:
                    self.nextItem = None
                cleanItem = item.strip()
                if self.needsKey :
                    self.newKey = cleanItem.strip('-[]')
                    self.groupDict[self.newKey] = []
                    self.needsKey = False
                    continue
                if cleanItem == '' and self.nextItem != None:
                    if self.nextItem.startswith('-[') and self.nextItem.endswith(']-') and self.nextItem != self.readList[
                        -1]:
                        self.needsKey = True
                    else:
                        continue
                else:
                    self.groupDict[self.newKey].append(cleanItem)
        if group == None :
            self.oldGroup = ()
            try:
                self.oldGroup = (switchReturn, '')
            except:
                self.oldGroup = ('None', 'None')
            if self.mode == 'list' :
                self.drawWidgets(group=True)
            self.theQuestion = Question(self.parent, self.groupDict, message='Please choose the group you want to move to,\n or right-click for more options:')
            self.theQuestion.parent.wait_window(self.theQuestion.top)
            if self.theQuestion.isSubmit :
                self.currentGroup = self.groupDict[switchReturn]
                self.statusVar.set('Current Group: ' + str(switchReturn))
            else :
                return False
            if move != None :
                self.groupDict[self.oldGroup[0]].remove(move)
                self.groupDict[switchReturn].append(move)
                return self.currentGroup
            else :
                return self.currentGroup

    def loadBox(self, isGroup=False, quiet=False, isMove=None):
        global firstLoad
        try:
            self.groupYes = False
            if quiet == False :
                self.file_type = [("Text files", "*.txt", "TEXT")]
                self.listFile = filedialog.askopenfile(mode='r', filetypes=self.file_type)
                if self.listFile == None :
                    return False
                self.isGroup = isGroup
                self.semiCheck = 0
                self.statusVar.set('')
            else :
                self.isGroup = isGroup
                self.semiCheck = 1
            if self.isGroup:
                self.fileFound = True
                if isMove != None :
                    self.groupList = self.findGroups(move=isMove)
                else :
                    self.groupList = self.findGroups(isMove)
                try:
                    self.listFile.close()
                except:
                    pass
                if self.groupList not in [False, None] :
                    self.drawWidgets(group=True)
                    self.listBox.delete(0, END)
                    for item in self.groupList :
                        self.listBox.insert(END, str(item))
                    self.fileFound = True
                    firstLoad = False
                    return True
                else :
                    if firstLoad and self.mode != 'group':
                        self.drawWidgets(group=True)
                    messagebox.showerror('Oops...', 'You didn\'t choose a group!')
                    firstLoad = False
                    return False

            else :
                self.drawWidgets(group=False)
            if self.listFile != None:
                self.textLines = self.listFile.read()
                self.textList = []
                self.readList = self.textLines.split(';')
                for item in self.textLines :
                    if ';' in item :
                        self.semiCheck += 1
                if self.semiCheck < 1:
                    self.fileFound = False
                    messagebox.showerror('Ut-Oh!', 'It appears that the text file you chose wasn\'t set-up right!')
                    self.listFile.close()
                    return False
                else :
                    for item in self.readList:
                        try :
                            self.nextItem = self.readList[self.readList.index(item) + 1].strip()
                        except IndexError :
                            self.nextItem = None
                        cleanItem = item.strip()
                        if cleanItem == '' and self.nextItem != None :
                            if self.nextItem.startswith('-[') and self.nextItem.endswith(']-') and self.nextItem != self.readList[-1]:
                                self.groupYes = True
                                break
                            else :
                                continue
                        else :
                            self.textList.append(cleanItem)
                    if self.groupYes :
                        self.loadBox(isGroup=True, quiet=True)
                        return True
                if self.textList == [''] or self.textList == []:
                    self.fileFound = False
                    messagebox.showerror('Ut-Oh!', 'It appears that the text file you chose wasn\'t set-up right!')
                    self.listFile.close()
                    return False
                else:
                    self.fileFound = True
                    self.listFile.close()
                    self.listBox.delete(0,END)
                    for item in self.textList :
                        self.listBox.insert(END, str(item))
                    return True
            else:
                self.fileFound = False
                return False
        except :
            self.fileFound = False
            messagebox.showerror('Ut-Oh!', 'An error has occurred opening that file!')
            return False

    def helper(self, op):
        if op == 'add/delete' :
            messagebox.showinfo('Add/Delete Buttons', 'To add an item to the list, type it in the entry box and press the "Add" button or hit <Enter>. To remove an item from the list, select it in the list box and press the "Delete" button.')
        elif op == 'browse/save' :
            messagebox.showinfo('Browse for List/Save List', 'To save the list/groups you\'ve created, press the "Save list" button and choose a file. To edit a list/groups you\'ve already made, press the "Browse for list" button and choose the list file you want to edit.')
        elif op == 'clear' :
            messagebox.showinfo('Clear List Button', 'To clear the list your editing, press the "Clear list" button.')

    def about(self, op):
        if op == 'about':
            messagebox.showinfo('About this program...','List Editor - GUI interface to Random Picker lists! Created by Shane1470!')
        elif op == 'github':
            if messagebox.askyesno('Are you sure about that?','Would you like to visit my GitHub page where this project is hosted?') == True:
                webbrowser.open('https://www.github.com/shane14705')
            else:
                return False

    def checkListBox(self):
        try :
            self.loadBox(isGroup=True, quiet=True, isMove=self.listBox.get(self.listBox.curselection()))
        except TclError :
            messagebox.showerror('Oops!', 'You haven\'t selected an item to move!')
            return False



root = Tk()
mainGUI = listGen(root)
mainGUI.mainloop()