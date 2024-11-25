from tkinter import*

window = Tk()
window.title("Santé mentale")
window.geometry("1080x720")
window.minsize(480, 360)
window.config(background='#41B77F')

def open_new_page():
    page = Tk()
    page.title("QCM")
    page.geometry("2160x1080")
    page.minsize(480, 360)
    page.config(background='#00CED1')
    


#premiere page

frame = Frame(window, bg="#41B77F")

#premier texte

label_title= Label(frame, text = "Bienvenue dans notre projet !", font=("Arial", 40), bg="#41B77F", fg="white")
label_title.pack()

#deuxieme texte
label_subtitle= Label(frame, text = "Vous allez maintenant répondre à un QCM", font=("Colibri", 30), bg="#41B77F", fg="white")
label_subtitle.pack()

frame.pack(expand=YES)

#bouton
bouton_page= Button(frame, text = "Commencer le QCM", font=("Courrier", 25), bg="white", fg="#41B77F", command= open_new_page)
bouton_page.pack()






window.mainloop()