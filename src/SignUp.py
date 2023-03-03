from tkinter import*
from tkinter import messagebox
from subprocess import call
import pymongo

MONGO_DATABASE = "Lavacar"
MONGO_COLLECTION = "Usuario"

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIMEOUT = 1000

#Base de Datos Local
mongo_uri = "mongodb://"+MONGO_HOST+":"+MONGO_PORT

client = pymongo.MongoClient(mongo_uri,serverSelectionTimeoutMS=MONGO_TIMEOUT)
database = client[MONGO_DATABASE]
collection_usuario = database[MONGO_COLLECTION]

#Ventana
root = Tk()
root.title('Sign Up')
root.geometry('925x500+300+200')
root.configure(bg = "#fff")
root.resizable(False, False)

def open_login_file():
    root.destroy()
    call(["python", "src/Login.py"])

def existe_usuario(username):
    existe = None
    try:
        for documento in collection_usuario.find():
            if username == documento["Username"]:
                existe = True
            client.close()
        return existe
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo Excedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as error:
        print("Fallo de Conexión con la Base de Datos "+error)
    except KeyError:
        None

def registrar_usuario(username, password):
    try:
        documento = { 
            "Username": username, 
            "Password": password}
        collection_usuario.insert_one(documento)
        messagebox.showinfo(message = "Se ha Registrado Correctamente")
        open_login_file()
        #user.delete(0, 'end')
        #passw.delete(0, 'end')
        #confirmpassw.delete(0, 'end')
        #user.insert(0, 'Usuario')
        #passw.config(show = '')
        #passw.insert(0, 'Contraseña')
        #confirmpassw.config(show = '')
        #confirmpassw.insert(0, 'Confirmar Contraseña')
    except pymongo.errors.ConnectionFailure as error:
        print(error)

def signup():
    username = user.get()
    password = passw.get()
    confirm_password = confirmpassw.get()

    if username == 'Usuario' or password == 'Contraseña' or confirm_password == 'Confirmar Contraseña':
        messagebox.showwarning(message = "Favor Introducir Todos los Campos")
    elif username == '' or password == '' or confirm_password == '':
        messagebox.showwarning(message = "Favor Introducir Todos los Campos")
    elif len(password) < 6:
        messagebox.showwarning(message = "La Contraseña debe contener 6 o más Caractéres")
    elif password != confirm_password:
        messagebox.showwarning(message = "La Contraseña de Confirmación no Coincide")
    else:
        if existe_usuario(username) == True:
            messagebox.showerror(message = "El Usuario "+username+" ya existe")
        else:
            registrar_usuario(username, password)

#Imagen Sign Up
img = PhotoImage(file = 'imgs/signup.png')
Label(root, image = img, bg = 'white').place(x = 50, y = 90)

frame = Frame(root, width = 350, height = 390, bg = "white")
frame.place(x = 480, y = 50)

#Widget Registrarse
heading = Label(frame, text = 'Registrarse', fg = '#57a1f8', bg = 'white', font = ('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x = 85, y = 5)

###################------------------------------------------------------------####################
def on_enter(e):
    username = ''
    for i in user.get():
        username = username + i
    if username == 'Usuario':
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
    password = ''
    for i in passw.get():
        password = password + i
    if password == 'Contraseña':
        passw.delete(0, 'end')
        passw.config(show = '*')
 
def on_leave(e):
    if passw.get() == '':
        passw.config(show = '')
        passw.insert(0, 'Contraseña')

#Entry Contraseña
passw = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
passw.place(x = 30, y = 150)
passw.insert(0, 'Contraseña')
passw.bind('<FocusIn>', on_enter)
passw.bind('<FocusOut>', on_leave)

Frame(frame, width = 295, height = 2, bg = 'black').place(x = 30, y = 177)

###################------------------------------------------------------------####################
def on_enter(e):
    confirm_password = ''
    for i in confirmpassw.get():
        confirm_password = confirm_password + i
    if confirm_password == 'Confirmar Contraseña':
        confirmpassw.delete(0, 'end')
        confirmpassw.config(show = '*')
 
def on_leave(e):
    if confirmpassw.get() == '':
        confirmpassw.config(show = '')
        confirmpassw.insert(0, 'Confirmar Contraseña')

#Entry Confirmar Contraseña
confirmpassw = Entry(frame, width = 25, fg = 'black', border = 0, bg = "white", font = ('Microsoft YaHei UI Light', 11))
confirmpassw.place(x = 30, y = 220)
confirmpassw.insert(0, 'Confirmar Contraseña')
confirmpassw.bind('<FocusIn>', on_enter)
confirmpassw.bind('<FocusOut>', on_leave)

Frame(frame, width = 295, height = 2, bg = 'black').place(x = 30, y = 247)

###################################################################################################

Button(frame, width = 39, pady = 7, text = 'Registrarse', bg = '#57a1f8', fg = 'white', border = 0, command = signup).place(x = 40, y = 280)
label = Label(frame, text = "Tengo una cuenta", fg = 'black', bg = 'white', font = ('Microsoft YaHei UI Light', 9))
label.place(x = 75, y = 340)

login = Button(frame, width = 9, text = 'Iniciar Sesión', border = 0, bg = 'white', cursor = 'hand2', fg = '#57a1f8', command = open_login_file)
login.place(x = 215, y = 340)

root.mainloop()