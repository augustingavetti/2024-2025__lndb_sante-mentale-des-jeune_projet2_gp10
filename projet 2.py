from tkinter import*

window = Tk()
window.title("Santé mentale")
window.geometry("1080x720")
window.minsize(720, 480)
window.config(background='#66CDAA')

def open_new_page():
    page = Tk()
    page.title("QCM")
    page.geometry("2160x1080")
    page.minsize(720, 480)
    page.config(background='#79CDCD')



#premiere page

frame = Frame(window, bg="#66CDAA")

#premier texte

label_title= Label(frame, text = "Bienvenue dans notre projet !", font=("Arial", 40), bg="#66CDAA", fg="white")
label_title.pack()

#deuxieme texte
label_subtitle= Label(frame, text = "Vous allez maintenant répondre à un QCM", font=("Colibri", 30), bg="#66CDAA", fg="white")
label_subtitle.pack()

frame.pack(expand=YES)

#bouton
bouton_page= Button(frame, text = "Commencer le QCM", font=("Courrier", 25), bg="white", fg="#66CDAA", command= open_new_page)
bouton_page.pack()



window.mainloop()