from tkinter import*

def Gui():
    gui = Tk()
    gui.title("Serveur Chat")
    gui.geometry("400x400")
    chatlog = Text(gui, bg="white")
    chatlog.config(state=DISABLED)
    sendbutton = Button(gui, bg='black', fg='white', text="SEND", )
    textbox = Text(gui, bg="white")
    chatlog.place(x=6, y=6, height=386, width=370)
    textbox.place(x=6, y=400, height=20, width=265)
    sendbutton.place(x=300, y=400, height=20, width=50)
    gui.mainloop()

if __name__  == "__main__":
    Gui()


