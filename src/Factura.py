from tkinter import*
from tkinter import messagebox
from tkinter.simpledialog import askstring
from tkinter import ttk
from subprocess import call
from docxtpl import DocxTemplate
import datetime
import pymongo

MONGO_DATABASE = "Lavacar"
MONGO_COLLECTION1 = "Factura"
MONGO_COLLECTION2 = "Cliente"

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIMEOUT = 1000

#Base de Datos Local
mongo_uri = "mongodb://"+MONGO_HOST+":"+MONGO_PORT

client = pymongo.MongoClient(mongo_uri,serverSelectionTimeoutMS=MONGO_TIMEOUT)
database = client[MONGO_DATABASE]
collection_factura = database[MONGO_COLLECTION1]
collection_cliente = database[MONGO_COLLECTION2]

#Ventana
root = Tk()
root.title("Factura")
root.geometry("1500x500+10+200")
root.configure(bg = "#fff")
root.resizable(False, False)

def open_lavacar_file():
    root.destroy()
    call(["python", "src/LavaCar.py"])

###################################################################################################
id_ultimo = 0
def mostrar_datos():
        global id_ultimo       
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_factura.find():
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id"]), 
                    values = (documento["Cedula"], documento["Fecha"], 
                              documento["Hora"], documento["Nombre"], 
                              documento["Apellido"], documento["Telefono"], 
                              documento["TipoLavado"], documento["IntensidadLavado"], 
                              documento["Subtotal"], documento["IVA"], 
                              documento["Total"])
                    )
                id_ultimo = int(documento["id"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None
          
def registrar_datos(cedula, fecha, hora, nombre, apellido, telefono, tipolavado, intensidadlavado, subtotal, iva, total):
    try:
        documento = {
            "id": int(id_ultimo+1), 
            "Cedula": cedula, 
            "Fecha": fecha,
            "Hora": hora,
            "Nombre": nombre,
            "Apellido": apellido,
            "Telefono": telefono,
            "TipoLavado": tipolavado,
            "IntensidadLavado": intensidadlavado,
            "Subtotal": subtotal,
            "IVA": iva,
            "Total": total}
        collection_factura.insert_one(documento)
    except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
        print("Tiempo Excedido "+errorTiempo)
    except pymongo.errors.ConnectionFailure as error:
        print("Fallo de Conexión con la Base de Datos "+error)
    except KeyError:
        None            

def cliente_existente():
    ced = askstring("Buscar Cliente", "Ingrese la Cédula", parent = frame)
    if ced != None:
        try:
            documento = collection_cliente.find({"Cedula": ced})[0]
            nombre.delete(0, "end")
            nombre.configure(fg = "black", bg = "white")
            nombre.insert(0, documento["Nombre"])
            apellido.delete(0, "end")
            apellido.configure(fg = "black", bg = "white")
            apellido.insert(0, documento["Apellido"])
            cedula.delete(0, "end")
            cedula.configure(fg = "black", bg = "white")
            cedula.insert(0, documento["Cedula"])
            telefono.delete(0, "end")
            telefono.configure(fg = "black", bg = "white")
            telefono.insert(0, documento["Telefono"])
        except IndexError as error:
            messagebox.showerror(message = "El Cliente con la Cédula "+ced+" no existe")
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

def generar_factura():
    doc = DocxTemplate("docs/factura_template.docx")

    null_values_cliente = ["", "nombre", "apellido", "cédula", "cedula", "teléfono", "telefono"]
    values_cliente = [nombre.get().lower(), apellido.get().lower(), cedula.get().lower(), telefono.get().lower()]
    non_null_values_servicio = ["Sencillo", "Pistola", "Cera", "Leve", "Normal", "Fuerte"]
    values_servicio = [tipolavado.get(), intensidad.get()]
    
    nullentry = False
    for value in values_cliente:
        if (value in null_values_cliente) == True:
            nullentry = True
            break

    for value in values_servicio:
        if (value in non_null_values_servicio) == False:
            nullentry = True
            break
        
    if nullentry != True:
        subtotal = 0.0
        preciotipo = 0.0
        preciointensidad = 0.0
        if tipolavado.get() == "Sencillo":
            preciotipo = float(10000)
            subtotal = subtotal + float(10000)
        elif tipolavado.get() == "Pistola":
            preciotipo = float(12500)
            subtotal = subtotal + float(12500)
        elif tipolavado.get() == "Cera":
            preciotipo = float(15000)
            subtotal = subtotal + float(15000)
        if intensidad.get() == "Leve":
            preciointensidad = float(1000)
            subtotal = subtotal + float(1000)
        elif intensidad.get() == "Normal":
            preciointensidad = float(1500)
            subtotal = subtotal + float(1500)
        elif intensidad.get() == "Fuerte":
            preciointensidad = float(2000)
            subtotal = subtotal + float(2000)
        
        iva = float((subtotal/100)*13)
        total = float(subtotal + iva)
        fecha = datetime.datetime.now().strftime("%Y-%m-%d")
        hora = datetime.datetime.now().strftime("%H:%M:%S")

        doc.render({"fecha": fecha, 
            "hora": hora,
            "nombre": nombre.get(),
            "apellido": apellido.get(),
            "tipolavado": tipolavado.get(),
            "intensidad": intensidad.get(),
            "preciotipo": preciotipo,
            "preciointensidad": preciointensidad,
            "subtotal": subtotal,
            "iva": iva,
            "total": total})
    
        doc_name = "docs/Factura_" + str(cedula.get()) + "_" + datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S") + ".docx"
        doc.save(doc_name)

        registrar_datos(cedula.get(), fecha, hora, nombre.get(), apellido.get(), telefono.get(), tipolavado.get(), intensidad.get(), subtotal, iva, total)
        mostrar_datos()
        nombre.delete(0, "end")
        nombre.insert(0, "Nombre")
        nombre.configure(fg = "white", bg = "#0a2f55")
        apellido.delete(0, "end")
        apellido.insert(0, "Apellido")
        apellido.configure(fg = "white", bg = "#0a2f55")
        cedula.delete(0, "end")
        cedula.insert(0, "Cédula")
        cedula.configure(fg = "white", bg = "#0a2f55")
        telefono.delete(0, "end")
        telefono.insert(0, "Teléfono")
        telefono.configure(fg = "white", bg = "#0a2f55")
        tipolavado.delete(0, "end")
        intensidad.delete(0, "end")

    else:
        messagebox.showwarning(message = "Alguno de los Campos se encuentra Vacío")

def buscar_factura():
    ced = askstring("Buscar Factura", "Ingrese la Cédula", parent = root)
    if ced != None:
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_factura.find({"Cedula": ced}):
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id"]), 
                    values = (documento["Cedula"], documento["Fecha"], 
                              documento["Hora"], documento["Nombre"], 
                              documento["Apellido"], documento["Telefono"], 
                              documento["TipoLavado"], documento["IntensidadLavado"], 
                              documento["Subtotal"], documento["IVA"], 
                              documento["Total"])
                    )
            client.close()
        except IndexError as error:
            messagebox.showerror(message = "La Factura con la Cédula "+ced+" no existe")
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None
    return

id_seleccionado = 0
def seleccionar_registro(event):
    global id_seleccionado
    id_seleccionado = tabla.item(tabla.selection())["text"]

def eliminar_factura():
    global id_seleccionado
    if id_seleccionado != 0:
        id_eliminar = {"id":id_seleccionado}
        try:
            collection_factura.delete_one(id_eliminar)
            messagebox.showinfo(message = "Factura eliminada correctamente")
            mostrar_datos()
        except IndexError as error:
            messagebox.showerror(message = "La Factura con ID "+ id_seleccionado +" no existe")
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None
    else:
        messagebox.showwarning(message = "Para seleccionar una Factura favor dar Doble Click")
###################################################################################################
#Sección
frame = Frame(root, width = 350, height = 500, bg = "#0a2f55")
frame.place(x = 0, y = 0)

heading = Label(frame, text = "Cliente", fg = "white", bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 18, "bold"))
heading.place(x = 125, y = 0)

Button(frame, width = 15, pady = 7, text = "¿Cliente Existente?", bg = "#0a2f55", fg = "white", border = 0, cursor = "hand2", command = cliente_existente).place(x = 220, y = 205)

def on_enter(e):
    name = ""
    for i in nombre.get():
        name = name + i
    if name == "Nombre":
        nombre.delete(0, "end")
        nombre.configure(fg = "black", bg = "white")
 
def on_leave(e):
    if nombre.get() == "" or nombre.get().lower() == "nombre":
        nombre.delete(0, "end")
        nombre.insert(0, "Nombre")
        nombre.configure(fg = "white", bg = "#0a2f55")

#Entry Nombre
nombre = Entry(frame, width = 15, fg = "white", border = 0, bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
nombre.place(x = 10, y = 50)
nombre.insert(0, "Nombre")
nombre.bind('<FocusIn>', on_enter)
nombre.bind('<FocusOut>', on_leave)
Frame(frame, width = 120, bg = "white").place(x = 10, y = 77)

###################################################################################################
def on_enter(e):
    apell = ""
    for i in apellido.get():
        apell = apell + i
    if apell == "Apellido":
        apellido.delete(0, "end")
        apellido.configure(fg = "black", bg = "white")
 
def on_leave(e):
    if apellido.get() == "" or apellido.get().lower() == "apellido":
        apellido.delete(0, "end")
        apellido.insert(0, "Apellido")
        apellido.configure(fg = "white", bg = "#0a2f55")

#Entry Apellido
apellido = Entry(frame, width = 15, fg = "white", border = 0, bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
apellido.place(x = 10, y = 100)
apellido.insert(0, "Apellido")
apellido.bind('<FocusIn>', on_enter)
apellido.bind('<FocusOut>', on_leave)
Frame(frame, width = 120, bg = "white").place(x = 10, y = 127)

###################################################################################################
def on_enter(e):
    ced = ""
    for i in cedula.get():
        ced = ced + i
    if ced == "Cédula":
        cedula.delete(0, "end")
        cedula.configure(fg = "black", bg = "white")
 
def on_leave(e):
    if cedula.get() == "" or cedula.get().lower() in ["cédula", "cedula"]:
        cedula.delete(0, "end")
        cedula.insert(0, "Cédula")
        cedula.configure(fg = "white", bg = "#0a2f55")

#Entry Cédula
cedula = Entry(frame, width = 15, fg = "white", border = 0, bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
cedula.place(x = 10, y = 150)
cedula.insert(0, "Cédula")
cedula.bind('<FocusIn>', on_enter)
cedula.bind('<FocusOut>', on_leave)
Frame(frame, width = 120, bg = "white").place(x = 10, y = 177)

###################################################################################################
def on_enter(e):
    tel = ""
    for i in telefono.get():
        tel = tel + i
    if tel == "Teléfono":
        telefono.delete(0, "end")
        telefono.configure(fg = "black", bg = "white")
 
def on_leave(e):
    if telefono.get() == "" or telefono.get().lower() in ["teléfono", "telefono"]:
        telefono.delete(0, "end")
        telefono.insert(0, "Teléfono")
        telefono.configure(fg = "white", bg = "#0a2f55")

#Entry Teléfono
telefono = Entry(frame, width = 15, fg = "white", border = 0, bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
telefono.place(x = 10, y = 200)
telefono.insert(0, "Teléfono")
telefono.bind('<FocusIn>', on_enter)
telefono.bind('<FocusOut>', on_leave)
Frame(frame, width = 120, bg = "white").place(x = 10, y = 227)

###################################################################################################
heading = Label(frame, text = "Servicio", fg = "white", bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 18, "bold"))
heading.place(x = 123, y = 270)

heading = Label(frame, text = "Tipo de Lavado", fg = "white", bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
heading.place(x = 10, y = 330)

#Entry Tipo de Lavado
tipolavado = ttk.Combobox(values = ["Sencillo", "Pistola", "Cera"])
tipolavado.place(x = 10, y = 360)

###################################################################################################
heading = Label(frame, text = "Intensidad", fg = "white", bg = "#0a2f55", font = ("Microsoft YaHei UI Light", 11))
heading.place(x = 195, y = 330)

#Entry Intensidad
intensidad = ttk.Combobox(values = ["Leve", "Normal", "Fuerte"])
intensidad.place(x = 195, y = 360)

Button(frame, width = 15, pady = 7, text = "Imprimir", bg = "white", fg = "black", border = 0, cursor = "hand2", command = generar_factura).place(x = 110, y = 450)

###################################################################################################
heading = Label(root, text = "Facturas", fg = "#0a2f55", bg = "white", font = ("Microsoft YaHei UI Light", 18, "bold"))
heading.place(x = 850, y = 0)

#Widget Tabla
tabla = ttk.Treeview(root, columns = 11)

#Definir las columnas de la Tabla
tabla['columns'] = ("Cedula", "Fecha", "Hora", "Nombre", "Apellido", "Telefono", "TipoLavado", "IntensidadLavado", "Subtotal", "IVA", "Total")
tabla.column("#0", anchor = "center", width = 50)
tabla.column("Cedula", anchor = "center", width = 90)
tabla.column("Fecha", anchor = "center", width = 75)
tabla.column("Hora", anchor = "center", width = 75)
tabla.column("Nombre", anchor = "center", width = 100)
tabla.column("Apellido", anchor = "center", width = 100)
tabla.column("Telefono", anchor = "center", width = 100)
tabla.column("TipoLavado", anchor = "center", width = 100)
tabla.column("IntensidadLavado", anchor = "center", width = 130)
tabla.column("Subtotal", anchor = "center", width = 90)
tabla.column("IVA", anchor = "center", width = 60)
tabla.column("Total", anchor = "center", width = 90)

#Crear Encabezados de la Tabla 
tabla.heading("#0", text = "Id", anchor = "center")
tabla.heading("Cedula", text = "Cédula", anchor = "center")
tabla.heading("Fecha", text = "Fecha", anchor = "center")
tabla.heading("Hora", text = "Hora", anchor = "center")
tabla.heading("Nombre", text = "Nombre", anchor = "center")
tabla.heading("Apellido", text = "Apellido", anchor = "center")
tabla.heading("Telefono", text = "Teléfono", anchor = "center")
tabla.heading("TipoLavado", text = "Tipo de Lavado", anchor = "center")
tabla.heading("IntensidadLavado", text = "Intensidad de Lavado", anchor = "center")
tabla.heading("IVA", text = "I.V.A", anchor = "center")
tabla.heading("Subtotal", text = "Subtotal", anchor = "center")
tabla.heading("Total", text = "Total", anchor = "center")
tabla.place(x = 390, y = 60, height = 300)
tabla.bind("<Double-Button-1>", seleccionar_registro)

#Widget Scrollbar
scrollbar = ttk.Scrollbar(root, orient = VERTICAL, command = tabla.yview)
tabla.configure(yscroll = scrollbar.set)
scrollbar.place(x = 1455, y = 60, height = 300)

###################################################################################################
#Botón Refrescar
Button(root, text = "Refrescar", bg = "#0a2f55", fg = "white", width = 10, cursor = "hand2", activebackground = "#00a4c5", activeforeground = "#0a2f55", command = mostrar_datos).place(x = 390, y = 370)

#Botón Buscar
Button(root, text = "Buscar", bg = "#0a2f55", fg = "white", width = 10, cursor = "hand2", activebackground = "#00a4c5", activeforeground = "#0a2f55", command = buscar_factura).place(x = 1200, y = 370)

#Botón Eliminar
Button(root, text = "Eliminar", bg = "#ad0000", fg = "white", width = 10, cursor = "hand2", activebackground = "#470000", activeforeground = "white", command = eliminar_factura).place(x = 1370, y = 370)

#Botón Inicio
Button(root, text = "Inicio", font = ("Shanti", 14), bg = "#0a2f55", fg = "white", width = 10, cursor = "hand2", activebackground = "#00a4c5", activeforeground = "#0a2f55", command = open_lavacar_file).place(x = 845, y = 450)



mostrar_datos()
root.mainloop()