from tkinter import *
from tkinter import messagebox
from tkinter import filedialog

import random
import os
import webbrowser


entryBoxReturn = None
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


class randomGui(Frame) :
    def __init__(self, parent):
        """

        :param parent: Root Tk() window

        """

        self.parent = parent
        super().__init__()
        self.parent.resizable(0, 0)
        try :
            self.parent.iconphoto(True, PhotoImage(file=os.getcwd() + "\\random-512.png"))
        except :
            pass
        self.parent.geometry("600x160+678+229")
        self.parent.title("Random Picker")
        self.parent.configure(background="#d9d9d9")
        self._bgcolor = '#d9d9d9'

        self.itemRemoval = BooleanVar()

        self.removeButton = Radiobutton()
        self.removeButton.place(relx=0.09, rely=0.13, relheight=0.16, relwidth=0.38)
        self.removeButton.configure(background=self._bgcolor)
        self.removeButton.configure(activebackground="#d9d9d9")
        self.removeButton.configure(activeforeground="#000000")
        self.removeButton.configure(disabledforeground="#a3a3a3")
        self.removeButton.configure(foreground="#000000")
        self.removeButton.configure(highlightbackground="#d9d9d9")
        self.removeButton.configure(highlightcolor="black")
        self.removeButton.configure(justify=LEFT)
        self.removeButton.configure(text='''Remove items that have been chosen''')
        self.removeButton.configure(value="True")
        self.removeButton.configure()
        self.removeButton.configure(variable=self.itemRemoval)
        self.removeButton.select()

        self.keepButton = Radiobutton()
        self.keepButton.place(relx=0.08, rely=0.31, relheight=0.16, relwidth=0.38)
        self.keepButton.configure(activebackground="#d9d9d9")
        self.keepButton.configure(activeforeground="#000000")
        self.keepButton.configure(disabledforeground="#a3a3a3")
        self.keepButton.configure(foreground="#000000")
        self.keepButton.configure(background=self._bgcolor)
        self.keepButton.configure(highlightbackground="#d9d9d9")
        self.keepButton.configure(highlightcolor="black")
        self.keepButton.configure(justify=LEFT)
        self.keepButton.configure(text='''Leave items that have been chosen''')
        self.keepButton.configure(value="False")
        self.keepButton.configure(variable=self.itemRemoval)
        self.keepButton.configure(width=232)

        self.browseButton = Button()
        self.browseButton.place(relx=0.62, rely=0.25, height=24, width=177)
        self.browseButton.configure(activebackground="#d9d9d9")
        self.browseButton.configure(activeforeground="#000000")
        self.browseButton.configure(background=self._bgcolor)
        self.browseButton.configure(command=self.findFile)
        self.browseButton.configure(disabledforeground="#a3a3a3")
        self.browseButton.configure(foreground="#000000")
        self.browseButton.configure(highlightbackground="#d9d9d9")
        self.browseButton.configure(highlightcolor="black")
        self.browseButton.configure(pady="0")
        self.browseButton.configure(text='''Browse for list file''')
        self.browseButton.configure(width=177)

        self.goButton = Button()
        self.goButton.place(relx=0.28, rely=0.69, height=24, width=87)
        self.goButton.configure(activebackground="#d9d9d9")
        self.goButton.configure(activeforeground="#000000")
        self.goButton.configure(cursor="arrow")
        self.goButton.configure(background=self._bgcolor)
        self.goButton.configure(disabledforeground="#a3a3a3")
        self.goButton.configure(foreground="#000000")
        self.goButton.configure(highlightbackground="#d9d9d9")
        self.goButton.configure(highlightcolor="black")
        self.goButton.configure(pady="0")
        self.goButton.configure(command=self.pickRandom)
        self.goButton.configure(text='''Get Random''')
        self.goButton.configure(width=87)

        self.resetButton = Button()
        self.resetButton.place(relx=0.45, rely=0.69, height=24, width=87)
        self.resetButton.configure(activebackground="#FF0000")
        self.resetButton.configure(activeforeground="#000000")
        self.resetButton.configure(background=self._bgcolor)
        self.resetButton.configure(cursor="arrow")
        self.resetButton.configure(disabledforeground="#a3a3a3")
        self.resetButton.configure(foreground="#FF0000")
        self.resetButton.configure(highlightbackground="#d9d9d9")
        self.resetButton.configure(highlightcolor="black")
        self.resetButton.configure(pady="0")
        self.resetButton.configure(text='''Reset''')
        self.resetButton.configure(command=self.resetList)

        self.groupButton = Button()
        self.groupButton.place(relx=0.62, rely=0.69, height=24, width=87)
        self.groupButton.configure(activebackground="#d9d9d9")
        self.groupButton.configure(activeforeground="#000000")
        self.groupButton.configure(background=self._bgcolor)
        self.groupButton.configure(cursor="arrow")
        self.groupButton.configure(disabledforeground="#a3a3a3")
        self.groupButton.configure(foreground="#000000")
        self.groupButton.configure(highlightbackground="#d9d9d9")
        self.groupButton.configure(highlightcolor="black")
        self.groupButton.configure(pady="0")
        self.groupButton.configure(text='''Group''')
        self.groupButton.configure(command=self.makeGroups)

        self.theMenu = Menu(self.parent, bg=self._bgcolor)
        self.parent.configure(menu=self.theMenu)

        self.aboutMenu = Menu(self.parent, tearoff=0)
        self.theMenu.add_cascade(menu=self.aboutMenu, activebackground="#d9d9d9", activeforeground="#111111",background="#d9d9d9", foreground="#000000", label="Info")
        self.aboutMenu.add_command(activebackground="#1E90FF",activeforeground="#000000",background="#d9d9d9",command=lambda:self.about('about'),foreground="#000000",label="About")
        self.aboutMenu.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.about('github'), foreground="#000000", label="GitHub")
        self.help = Menu(self.parent, tearoff=0)
        self.theMenu.add_cascade(menu=self.help,activebackground="#d9d9d9",activeforeground="#111111",background="#d9d9d9",foreground="#000000",label="Help")
        self.help.add_command(activebackground="#1E90FF",activeforeground="#000000",background="#d9d9d9",command=lambda:self.helper('removeItems'),foreground="#000000",label="Remove/Leave Items")
        self.help.add_command(activebackground="#1E90FF",activeforeground="#000000",background="#d9d9d9",command=lambda:self.helper('GO/Reset'),foreground="#000000",label="Get Random/Reset Buttons")
        self.help.add_command(activebackground="#1E90FF",activeforeground="#000000",background="#d9d9d9",command=lambda:self.helper('Browse'),foreground="#000000",label="Browse for List File")
        self.help.add_command(activebackground="#1E90FF", activeforeground="#000000", background="#d9d9d9",command=lambda: self.helper('group'), foreground="#000000", label="Group")

        self.fileFound = False
        self.textList = []

    def findFile(self, op=1):
        if op == 1 :
            try :
                self.file_type = [("Text files", "*.txt", "TEXT")]
                self.listFile = filedialog.askopenfile(mode='r', filetypes=self.file_type)
                if self.listFile != None :
                    self.textLines = self.listFile.read()
                    self.textList = []
                    self.readList = self.textLines.split(';')
                    for item in self.readList :
                        try :
                            self.nextItem = self.readList[self.readList.index(item) + 1].strip()
                        except IndexError :
                            self.nextItem = None
                        cleanItem = item.strip()
                        if cleanItem == '' and self.nextItem != None:
                            if self.nextItem.startswith('-[') and self.nextItem.endswith(']-') and self.nextItem != self.readList[-1]:
                                messagebox.showerror('Oops...','This appears to be a group file! If you want to edit it, please open it in the included List Editor program.')
                                self.fileFound = False
                                self.listFile.close()
                                return False
                            else :
                                continue
                        self.textList.append(cleanItem)
                    if ';' not in self.textLines :
                        self.fileFound = False
                        messagebox.showerror('Ut-Oh!', 'It appears that the text file you chose wasn\'t set-up right!')
                        self.listFile.close()
                        return False
                    elif self.textList == [''] :
                        self.fileFound = False
                        messagebox.showerror('Ut-Oh!', 'It appears that the text file you chose wasn\'t set-up right!')
                        self.listFile.close()
                        return False
                    else :
                        self.fileFound = True
                        self.listFile.close()
                else :
                    self.fileFound = False
                    try :
                        self.listFile.close()
                    except :
                        pass
                    return False
            except :
                self.fileFound = False
                self.listFile.close()
                messagebox.showerror('Ut-Oh!', 'An error has occurred opening that file!')
                return False
        elif op == 2 :
            if self.fileFound == True :
                try :
                    self.resetFile = open(self.listFile.name, mode='r')
                    self.textLines = self.resetFile.read()
                    self.textList = []
                    self.readList = self.textLines.split(';')
                    for item in self.readList :
                        cleanItem = item.strip()
                        if cleanItem == '' :
                            continue
                        else :
                            self.textList.append(cleanItem)
                    if self.textList == [''] :
                        self.fileFound = False
                        self.textList = []
                        messagebox.showerror('Ut-Oh!', 'It appears that the text file you chose wasn\'t set-up right!')
                        self.resetFile.close()
                        return False
                    else :
                        self.fileFound = True
                        self.resetFile.close()
                except :
                    self.fileFound = False
                    self.textList = []
                    messagebox.showerror('Ut-Oh!', 'An error has occurred reading that file!')
                    self.resetFile.close()
                    return False
            else :
                self.fileFound = False
                messagebox.showerror('Ut-Oh!', 'You don\'t even have a file open!')

    def pickRandom(self, quiet=False, quietRemove=False):
        if not quiet :
            if self.fileFound != True :
                messagebox.showerror('Ut-Oh!', 'You haven\'t chosen a text file yet!')
                return False
            else :
                if self.textList == [] :
                    messagebox.showwarning('Oops...', 'I ran out of choices! Hit reset to start over or choose another list!')
                    return False
                theChoice = str(random.choice(self.textList))
                if theChoice == '' :
                    messagebox.showerror('Ut-Oh!', 'I somehow ended up with a blank item as a choice!')
                    return False
                else :
                    messagebox.showinfo('Drumroll please...', 'I choose ' + theChoice + '!')
                    if self.itemRemoval.get() == True :
                        self.textList.remove(theChoice)
                        return None
                    else :
                        return None
        else :
            if self.fileFound != True :
                messagebox.showerror('Ut-Oh!', 'You haven\'t chosen a text file yet!')
                return False
            else :
                if self.textList == [] :
                    return False
                theChoice = str(random.choice(self.textList))
                if theChoice == '' :
                    return False
                else :
                    if quietRemove == True :
                        self.textList.remove(theChoice)
                        return theChoice
                    else :
                        return theChoice

    def resetList(self, quiet=False):
        self.findFile(op=2)
        if not quiet :
            if self.textList != [] :
                messagebox.showinfo('OK!', 'Your list has been reset and you should be set to go!')
                return True
            elif self.fileFound == False :
                return False
            else :
                messagebox.showerror('Ut-Oh!', 'An error has occurred resetting the list! Please re-choose your file.')
                return None
        else :
            if self.textList != [] :
                return True
            elif self.fileFound == False :
                return False
            else :
                messagebox.showerror('Ut-Oh!', 'An error has occurred resetting the list! Please re-choose your file.')
                return None

    def saveGroup(self,groupDict):
        try :
            self.partList = []
            self.groupDict = groupDict
            self.file_type = [("Text files", "*.txt", "TEXT")]
            self.saveFile = filedialog.asksaveasfile(mode='w', filetypes=self.file_type, defaultextension='.txt')
            if self.saveFile != None :
                for item in sorted(self.groupDict.keys()) :
                    self.saveFile.write(';-[' + str(item) + ']-; \n \n')
                    self.partList = self.groupDict[item].split(';')
                    for part in self.partList :
                        self.saveFile.write(str(part)+ '; \n')
                    self.saveFile.write('\n')
                self.saveFile.close()
                self.yayOrNay = messagebox.askyesno('Group File Created!', 'Would you like to open the new group file?')
                if self.yayOrNay == True :
                    webbrowser.open(self.saveFile.name)
                else :
                    pass
            else :
                return False
        except:
            messagebox.showerror('Ut-Oh!', 'An error occurred saving the file! Please try again!')
            return False

    def about(self, op):
        if op == 'about' :
            messagebox.showinfo('About this program...', 'Random Picker - GUI interface to random! Created by Shane1470!')
        elif op == 'github' :
            if messagebox.askyesno('Are you sure about that?', 'Would you like to visit my GitHub page where this project is hosted?') ==  True:
                webbrowser.open('https://www.github.com/shane14705')
            else :
                pass

    def helper(self, op):
        if op == 'removeItems' :
            messagebox.showinfo('Help', 'Depending on which of these buttons you have selected, the program will either remove items after they\'ve been chosen, or leave them so they can get picked again.')
        elif op == 'GO/Reset' :
            messagebox.showinfo('Help', 'Clicking the "Get Random" button will have the program pick a random item from the list. Clicking the "Reset" button will cause the list to be reset so items that were removed can be picked again.')
        elif op == 'Browse' :
            messagebox.showinfo('Help', 'Use this button to find and open a list compatible with the Random Picker program. If you need to create one of these lists, please use the included List Generator program.')
        elif op == 'group' :
            messagebox.showinfo('Help', 'To randomly sort your list into groups, press the "Group" button after selecting your list. To edit a group file, please open it in the included List Editor program.')

    def makeGroups(self):
        global entryBoxReturn
        global buttonSubmitted
        if self.fileFound != True :
            messagebox.showerror('Ut-Oh!', 'You haven\'t chosen a text file yet!')
            return False
        self.entryGUI = entryDialog(self.parent, 'How many items in each group?', justNumbers=True)
        self.entryGUI.parent.wait_window(self.entryGUI.top)
        if self.entryGUI.isSubmit == False :
            return False
        self.resetList(quiet=True)
        self.entryBox = entryBoxReturn.strip()
        self.incrementer = 1
        self.groupNumber = 1
        self.groups = {}
        self.itemGroups = []
        self.listLen = len(self.textList)
        if self.entryBox.startswith('0') :
            messagebox.showerror('Ut-Oh!', 'That\'s not a valid number!')
            return False
        elif int(self.entryBox) > self.listLen :
            messagebox.showerror('Ut-Oh!', 'That\'s more items than are in your list!')
            return False
        else :
            if self.listLen % int(self.entryBox) :
                if messagebox.askyesno('Are you sure about that?', 'The number of items you chose will cause one group to have less items than the others. Would you like to continue?') == True :
                    pass
                else:
                    return False
        for item in range(1, self.listLen + 1) :
            self.incrementer += 1
            if len(self.itemGroups) == int(self.entryBox):
                self.groups['Group ' + str(self.groupNumber)] = str(';'.join(self.itemGroups))
                self.groupNumber += 1
                self.itemGroups = []
                self.itemGroups.append(str(self.pickRandom(quiet=True, quietRemove=True)))
            else :
                self.itemGroups.append(str(self.pickRandom(quiet=True, quietRemove=True)))
        if self.itemGroups != [] :
            self.groups['Group ' + str(self.groupNumber)] = str(';'.join(self.itemGroups))
        self.saveGroup(self.groups)
        self.resetList(quiet=True)



root = Tk()
mainGUI = randomGui(root)
mainGUI.mainloop()