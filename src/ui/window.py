from tkinter import *


def sendMessage():
    showMessage.configure(state="normal")
    message = createMessage.get()
    createMessage.delete(0, END)
    showMessage.insert(END, message + "\n")
    showMessage.configure(state="disabled")


def removeLogin():
    login.destroy()
    chatWindow.deiconify()


chatWindow = Tk()
chatWindow.title("Chat Room")

showMessage = Text(chatWindow, width=50, height=30)
showMessage.configure(state="disabled")
showMessage.pack()

createMessage = Entry(chatWindow, width=45)
createMessage.pack()

btn_sendMessage = Button(chatWindow, text="Send", width=10, height=3, bg="white", fg="black", command=sendMessage)
btn_sendMessage.pack()

chatWindow.withdraw()

login = Toplevel()
login.title('login')
lbl_greeting = Label(login, text="Press START to enter the chatroom")
lbl_greeting.pack()
btn_login = Button(login, text="START", width=10, height=3, bg="white", fg="black", command=removeLogin)
btn_login.pack()

chatWindow.mainloop()
