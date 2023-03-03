from tkinter import*
from tkinter import messagebox
from subprocess import call

#Ventana
root = Tk()
root.title('Login')
root.geometry('925x500+300+200')
root.configure(bg = "#fff")
root.resizable(False, False)

def open_lavacar_file():
    root.destroy()
    call(["python", "src/LavaCar.py"])

def open_signup_file():
    root.destroy()
    call(["python", "src/SignUp.py"])

def signin():
    username = user.get()
    password = passw.get()

    if username == 'Admin' and password == '123':
        print('Inicio de Sesión Correcto')
        open_lavacar_file()
        


#Imagen Login
img = PhotoImage(file = 'imgs/login.png')
Label(root, image = img, bg = 'white').place(x = 50, y = 50)

frame = Frame(root, width = 350, height = 350, bg = "white")
frame.place(x = 480, y = 70)

#Widget Iniciar Sesión
heading = Label(frame, text = 'Iniciar Sesión', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x = 75, y = 5)

###################------------------------------------------------------------####################
def on_enter(e):
    user.delete(0, 'end')
 
def on_leave(e):
    if user.get() == '':
        user.insert(0, 'Usuario')

#Entry Usuario
user = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
user.place(x = 30, y = 80)
user.insert(0, 'Usuario')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width = 295, height = 2, bg = 'black').place(x = 30, y = 107)

###################------------------------------------------------------------####################
def on_enter(e):
    passw.delete(0, 'end')
 
def on_leave(e):
    if passw.get() == '':
        passw.insert(0, 'Contraseña')

#Entry Contraseña
passw = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
passw.place(x = 30, y = 150)
passw.insert(0, 'Contraseña')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>', on_leave)

Frame(frame, width = 295, height = 2, bg = 'black').place(x = 30, y = 177)

###################################################################################################

Button(frame, width = 39, pady = 7, text = 'Iniciar Sesión', bg = '#57a1f8', fg = 'white', border = 0, command = signin).place(x = 40, y = 204)
label = Label(frame, text = "¿No tiene una cuenta?", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
label.place(x = 75, y = 270)

sign_up = Button(frame, width = 8, text = 'Registrarse', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = open_signup_file)
sign_up.place(x = 215, y = 270)


root.mainloop()
