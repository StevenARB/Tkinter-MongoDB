import pymongo
import tkinter as tk
import pyglet
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk

MONGO_DATABASE = "Lavacar"
MONGO_COLLECTION1 = "Cliente"
MONGO_COLLECTION2 = "Vehiculo"
MONGO_COLLECTION3 = "Servicio"
MONGO_COLLECTION4 = "Establecimiento"

MONGO_HOST = "localhost"
MONGO_PORT = "27017"
MONGO_TIMEOUT = 1000

#Base de Datos Local
mongo_uri = "mongodb://"+MONGO_HOST+":"+MONGO_PORT
#Base de Datos Remota (Mongo Atlas)
#mongo_uri = "mongodb+srv://sretana:prueba123@simulacion.kqky1jw.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(mongo_uri,serverSelectionTimeoutMS=MONGO_TIMEOUT)
database = client[MONGO_DATABASE]
collection_cliente = database[MONGO_COLLECTION1]
collection_vehiculo = database[MONGO_COLLECTION2]
collection_servicio = database[MONGO_COLLECTION3]
collection_establecimiento = database[MONGO_COLLECTION4]
ver_id = None

def limpiar_widgets(ventana):
    for widget in ventana.winfo_children():
        widget.destroy()

def limpiar_label(ver_id):
    if ver_id == None:
        return None
    else:
        ver_id.destroy()

def mostrar_ventana_Inicio():
    limpiar_widgets(ventana_cliente)
    limpiar_widgets(ventana_vehiculo)
    limpiar_widgets(ventana_servicio)
    limpiar_widgets(ventana_establecimiento)
    ventana_inicio.tkraise()
    ventana_inicio.pack_propagate(False)

    def ingresos_totales():
        global cuenta_total
        cuenta_total = 0.0
        try:
            for documento in collection_establecimiento.find():
                cuenta_total = cuenta_total + float(documento["Ingreso_Total"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def vehiculo_atendido():
        global cuenta_ultimo
        cuenta_ultimo = None
        try:
            for documento in collection_vehiculo.find():
                cuenta_ultimo = str(documento["Placa"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def gasto_litros():
        global gasto_litros
        gasto_litros = 0.0
        try:
            for documento in collection_servicio.find():
                gasto_litros = gasto_litros + float(documento["Agua_Litros"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None
        
        #Widget Label Texto Ingresos Totales
        tk.Label(
            ventana_inicio, 
            text = "Ingresos Totales", 
            bg = bg_color, fg = "#0a2f55", 
            font = ("Shandi", 20)
            ).grid(row = 2, column = 0, padx = 140)
        
        #Widget Label Float Ingresos Totales
        tk.Label(
            ventana_inicio, 
            text = cuenta_total, 
            bg = bg_color, fg = "#b24400", 
            font = ("Ubuntu", 20)
            ).grid(row = 3, column = 0, padx = 140)

        #Widget Label Texto Vehiculo Reciente
        tk.Label(
            ventana_inicio, 
            text = "Vehiculo Reciente", 
            bg = bg_color, fg = "#0a2f55", 
            font = ("Shandi", 20)
            ).grid(row = 2, column = 1)

        #Widget Label Texto Vehiculo Reciente
        tk.Label(
            ventana_inicio, 
            text = cuenta_ultimo, 
            bg = bg_color, fg = "#b24400", 
            font = ("Ubuntu", 20)
            ).grid(row = 3, column = 1)

        #Widget Label Texto Gasto Litros
        tk.Label(
            ventana_inicio, 
            text = "Gasto de Agua", 
            bg = bg_color, fg = "#0a2f55", 
            font = ("Shandi", 20)
            ).grid(row = 2, column = 2, padx = 100)

        #Widget Label Float Gasto Litros
        tk.Label(
            ventana_inicio, 
            text = gasto_litros, 
            bg = bg_color, fg = "#b24400", 
            font = ("Ubuntu", 20)
            ).grid(row = 3, column = 2, padx = 100)

    #Widget Label Inicio
    tk.Label(
        ventana_inicio, 
        text = "Inicio", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Ubuntu", 20)
        ).grid(row = 0, column = 0, columnspan = 4)

    #Widget Logo Lava Carros
    logo_image = ImageTk.PhotoImage(file = "imgs/LavacarIcon.png")
    logo_widget = tk.Label(ventana_inicio, image = logo_image, bg = bg_color)
    logo_widget.image = logo_image
    logo_widget.grid(row = 1, column = 0, columnspan = 4)

    ingresos_totales()
    vehiculo_atendido()
    gasto_litros()

def mostrar_ventana_cliente():
    def mostrar_datos():
        global id_ultimo
        id_ultimo = 0
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_cliente.find():
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id_Cliente"]), 
                    values = (documento["Nombre"], documento["Apellido"], documento["Cedula"], documento["Telefono"])
                    )
                id_ultimo = int(documento["id_Cliente"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def insertar_datos():
        if len(nombre.get()) != 0 and len(apellido.get()) != 0 and len(cedula.get()) != 0 and len(telefono.get()) != 0:
            try:
                documento = {
                    "id_Cliente": int(id_ultimo+1), 
                    "Nombre": nombre.get(), 
                    "Apellido": apellido.get(), 
                    "Cedula": cedula.get(),
                    "Telefono": telefono.get()}
                collection_cliente.insert_one(documento)
                nombre.delete(0, END)
                apellido.delete(0, END)
                cedula.delete(0, END)
                telefono.delete(0, END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror(message = "Campos Vacíos")
        mostrar_datos()

    def modificar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        if len(nombre.get()) !=0 and len(apellido.get()) !=0 and len(cedula.get()) !=0 and len(telefono.get()) !=0:
            try:
                idBuscar = {"id_Cliente":id_local}
                nuevosValores = {
                    "$set":{
                        "id_Cliente": int(id_local), 
                        "Nombre": nombre.get(), 
                        "Apellido": apellido.get(), 
                        "Cedula": cedula.get(),
                        "Telefono": telefono.get()}
                        }
                collection_cliente.update_one(idBuscar, nuevosValores)
                nombre.delete(0,END)
                apellido.delete(0,END)
                cedula.delete(0,END)
                telefono.delete(0,END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror("Los Campos no pueden estar Vacíos")
        mostrar_datos()
        crear["state"] = "normal"
        modificar["state"] = "disabled"

    def eliminar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        try:
            idBuscar = {"id_Cliente":id_local}
            collection_cliente.delete_one(idBuscar)
            nombre.delete(0,END)
            apellido.delete(0,END)
            cedula.delete(0,END)
            telefono.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
        crear["state"] = "normal"
        modificar["state"] = "disabled"
        eliminar["state"] = "disabled"
        mostrar_datos()

    def seleccionar_registro(event):
        global id_local, ver_id
        id_local = tabla.item(tabla.selection())["text"]
        documento = collection_cliente.find({"id_Cliente": id_local})[0]
        limpiar_label(ver_id)
        ver_id = Label(ventana_cliente, text = str(id_local), font = ("Shanti", 16), bg = bg_color)
        ver_id.grid(row = 5, column = 0) 
        nombre.delete(0, END)
        nombre.insert(0, documento["Nombre"])
        apellido.delete(0, END)
        apellido.insert(0, documento["Apellido"])
        cedula.delete(0, END)
        cedula.insert(0, documento["Cedula"])
        telefono.delete(0, END)
        telefono.insert(0, documento["Telefono"])
        crear["state"] = "disabled"
        modificar["state"] = "normal"
        eliminar["state"] = "normal"
    
    #Limpiar la ventana y sobreexponer la nueva ventana        
    limpiar_widgets(ventana_inicio)
    ventana_cliente.tkraise()

    #Widget Label Cliente
    tk.Label(
        ventana_cliente, 
        text = "Cliente", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Ubuntu", 18)
        ).grid(row = 0, column = 0, columnspan = 4)

    #Widget Tabla
    tabla = ttk.Treeview(ventana_cliente, columns=4)

    #Definir las columnas de la Tabla
    tabla['columns'] = ("Nombre", "Apellido", "Cedula", "Telefono")
    tabla.column("#0", anchor = "center", width = 70)
    tabla.column("Nombre", anchor = "center", width = 120)
    tabla.column("Apellido", anchor = "center", width = 120)
    tabla.column("Cedula", anchor = "center", width = 120)
    tabla.column("Telefono", anchor = "center", width = 120)

    #Crear Encabezados de la Tabla 
    tabla.heading("#0", text = "Id", anchor = "center")
    tabla.heading("Nombre", text = "Nombre", anchor = "center")
    tabla.heading("Apellido", text = "Apellido", anchor = "center")
    tabla.heading("Cedula", text = "Cédula", anchor = "center")
    tabla.heading("Telefono", text = "Teléfono", anchor = "center")
    tabla.grid(row = 2, column = 0, columnspan = 6, sticky = 'nsew')
    tabla.bind("<Double-Button-1>", seleccionar_registro)

    #Widget Scrollbar
    scrollbar = ttk.Scrollbar(ventana_cliente, orient = tk.VERTICAL, command = tabla.yview)
    tabla.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 2, column = 6, sticky = 'ns')

    #Widget Label CRUD
    tk.Label(
        ventana_cliente, 
        text = "CRUD", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Shanti", 20)
        ).grid(row = 3, column = 0, columnspan = 4)

    #Widget Label Id
    tk.Label(ventana_cliente, text = "Id", font = ("Shanti", 12), bg = bg_color).grid(row = 4, column = 0)
    ver_id = tk.Label(ventana_cliente, text = "", font = ("Shanti", 16), bg=bg_color)
    ver_id.grid(row = 5, column = 0)

    #Widget Label y Entry Nombre
    tk.Label(ventana_cliente, text = "Nombre", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 0)
    nombre = Entry(ventana_cliente)
    nombre.grid(row = 7, column = 0)

    #Widget Label y Entry Apellido
    tk.Label(ventana_cliente, text = "Apellido", font = ("Shanti", 12), bg = bg_color).grid(row = 8, column = 0)
    apellido = Entry(ventana_cliente)
    apellido.grid(row = 9, column = 0)

    #Widget Label y Entry Cédula
    tk.Label(ventana_cliente, text = "Cédula", font = ("Shanti", 12), bg = bg_color).grid(row = 10, column = 0)
    cedula = Entry(ventana_cliente)
    cedula.grid(row = 11, column = 0)

    #Widget Label y Entry Teléfono
    tk.Label(ventana_cliente, text = "Teléfono", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 1)
    telefono = Entry(ventana_cliente)
    telefono.grid(row = 7, column = 1)

    #Widget Botón Crear
    crear = tk.Button(
        ventana_cliente, 
        text= "Crear", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 8, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = insertar_datos
        )
    crear.grid(row = 7, column = 3)

    #Widget Botón Modificar
    modificar = tk.Button(
        ventana_cliente, 
        text = "Modificar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = modificar_datos
        )
    modificar.grid(row = 9, column = 3)
    modificar["state"] = "disabled"

    #Widget Botón Eliminar
    eliminar = tk.Button(
        ventana_cliente, 
        text = "Eliminar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = eliminar_datos
        )
    eliminar.grid(row = 11, column = 3)
    eliminar["state"] = "disabled"     

    #Widget Botón Inicio
    tk.Label(ventana_cliente, text = "", bg=bg_color).grid(row = 12, column = 0)
    tk.Button(
        ventana_cliente, 
        text = "Inicio", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 10, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = mostrar_ventana_Inicio
        ).grid(row = 13, column = 0, columnspan = 6)
    tk.Label(ventana_cliente, text = "", bg = bg_color).grid(row = 14, column = 0)

    #Mostrar los Datos de la Colección Cliente
    mostrar_datos()

def mostrar_ventana_vehiculo():
    def mostrar_datos():
        global id_ultimo
        id_ultimo = 0
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_vehiculo.find():
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id_Vehiculo"]), 
                    values = (documento["Placa"], documento["Marca"], documento["Modelo"], documento["Tipo"], documento["Color"], documento["N_Puertas"])
                    )
                id_ultimo = int(documento["id_Vehiculo"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def insertar_datos():
        if len(placa.get()) != 0 and len(marca.get()) != 0 and len(modelo.get()) != 0 and len(tipo.get()) != 0 and len(color.get()) != 0 and len(n_puertas.get()) != 0:
            try:
                documento = {
                    "id_Vehiculo": int(id_ultimo+1), 
                    "Placa": placa.get(), 
                    "Marca": marca.get(), 
                    "Modelo": modelo.get(),
					"Tipo": tipo.get(),
					"Color": color.get(),
					"N_Puertas": n_puertas.get()}
                collection_vehiculo.insert_one(documento)
                placa.delete(0, END)
                marca.delete(0, END)
                modelo.delete(0, END)
                tipo.delete(0, END)
                color.delete(0, END)
                n_puertas.delete(0, END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror(message = "Campos Vacíos")
        mostrar_datos()

    def modificar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        if len(placa.get()) != 0 and len(marca.get()) != 0 and len(modelo.get()) != 0 and len(tipo.get()) != 0 and len(color.get()) != 0 and len(n_puertas.get()) != 0:
            try:
                idBuscar = {"id_Vehiculo":id_local}
                nuevosValores = {
                    "$set":{
                        "id_Vehiculo": int(id_local), 
                    	"Placa": placa.get(), 
                    	"Marca": marca.get(), 
                    	"Modelo": modelo.get(),
						"Tipo": tipo.get(),
						"Color": color.get(),
						"N_Puertas": n_puertas.get()}
                        }
                collection_vehiculo.update_one(idBuscar, nuevosValores)
                placa.delete(0, END)
                marca.delete(0, END)
                modelo.delete(0, END)
                tipo.delete(0, END)
                color.delete(0, END)
                n_puertas.delete(0, END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror("Los Campos no pueden estar Vacíos")
        mostrar_datos()
        crear["state"] = "normal"
        modificar["state"] = "disabled"

    def eliminar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        try:
            idBuscar = {"id_Vehiculo":id_local}
            collection_vehiculo.delete_one(idBuscar)
            placa.delete(0, END)
            marca.delete(0, END)
            modelo.delete(0, END)
            tipo.delete(0, END)
            color.delete(0, END)
            n_puertas.delete(0, END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
        crear["state"] = "normal"
        modificar["state"] = "disabled"
        eliminar["state"] = "disabled"
        mostrar_datos()

    def seleccionar_registro(event):
        global id_local, ver_id
        id_local = tabla.item(tabla.selection())["text"]
        documento = collection_vehiculo.find({"id_Vehiculo": id_local})[0]
        limpiar_label(ver_id)
        ver_id = Label(ventana_vehiculo, text = str(id_local), font = ("Shanti", 16), bg = bg_color)
        ver_id.grid(row = 5, column = 0) 
        placa.delete(0, END)
        placa.insert(0, documento["Placa"])
        marca.delete(0, END)
        marca.insert(0, documento["Marca"])
        modelo.delete(0, END)
        modelo.insert(0, documento["Modelo"])
        tipo.delete(0, END)
        tipo.insert(0, documento["Tipo"])
        color.delete(0, END)
        color.insert(0, documento["Color"])
        n_puertas.delete(0, END)
        n_puertas.insert(0, documento["N_Puertas"])
        crear["state"] = "disabled"
        modificar["state"] = "normal"
        eliminar["state"] = "normal"
    
    #Limpiar la ventana y sobreexponer la nueva ventana        
    limpiar_widgets(ventana_inicio)
    ventana_vehiculo.tkraise()

    #Widget Label Vehiculo
    tk.Label(
        ventana_vehiculo, 
        text = "Vehiculo", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Ubuntu", 18)
        ).grid(row = 0, column = 0, columnspan = 7)

    #Widget Tabla
    tabla = ttk.Treeview(ventana_vehiculo, columns = 7)

    #Definir las columnas de la Tabla
    tabla['columns'] = ("Placa", "Marca", "Modelo", "Tipo", "Color", "N_Puertas")
    tabla.column("#0", anchor = "center", width = 70)
    tabla.column("Placa", anchor = "center", width = 120)
    tabla.column("Marca", anchor = "center", width = 120)
    tabla.column("Modelo", anchor = "center", width = 120)
    tabla.column("Tipo", anchor = "center", width = 120)
    tabla.column("Color", anchor = "center", width = 120)
    tabla.column("N_Puertas", anchor = "center", width = 70)

    #Crear Encabezados de la Tabla 
    tabla.heading("#0", text = "Id", anchor = "center")
    tabla.heading("Placa", text = "Placa", anchor = "center")
    tabla.heading("Marca", text = "Marca", anchor = "center")
    tabla.heading("Modelo", text = "Modelo", anchor = "center")
    tabla.heading("Tipo", text = "Tipo", anchor = "center")
    tabla.heading("Color", text = "Color", anchor = "center")
    tabla.heading("N_Puertas", text = "Puertas", anchor = "center")
    tabla.grid(row = 2, column = 0, columnspan = 7, sticky = 'nsew')
    tabla.bind("<Double-Button-1>", seleccionar_registro)

    #Widget Scrollbar
    scrollbar = ttk.Scrollbar(ventana_vehiculo, orient = tk.VERTICAL, command = tabla.yview)
    tabla.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 2, column = 8, sticky = 'ns')

    #Widget Label CRUD
    tk.Label(
        ventana_vehiculo, 
        text = "CRUD", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Shanti", 20)
        ).grid(row = 3, column = 0, columnspan = 4)

    #Widget Label Id
    tk.Label(ventana_vehiculo, text = "Id", font = ("Shanti", 12), bg = bg_color).grid(row = 4, column = 0)
    ver_id = tk.Label(ventana_vehiculo, text = "", font = ("Shanti", 16), bg=bg_color)
    ver_id.grid(row = 5, column = 0)

    #Widget Label y Entry Placa
    tk.Label(ventana_vehiculo, text = "Placa", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 0)
    placa = Entry(ventana_vehiculo)
    placa.grid(row = 7, column = 0)

    #Widget Label y Entry Marca
    tk.Label(ventana_vehiculo, text = "Marca", font = ("Shanti", 12), bg = bg_color).grid(row = 8, column = 0)
    marca = Entry(ventana_vehiculo)
    marca.grid(row = 9, column = 0)

    #Widget Label y Entry Modelo
    tk.Label(ventana_vehiculo, text = "Modelo", font = ("Shanti", 12), bg = bg_color).grid(row = 10, column = 0)
    modelo = Entry(ventana_vehiculo)
    modelo.grid(row = 11, column = 0)

	#Widget Label y Entry Tipo
    tk.Label(ventana_vehiculo, text = "Tipo", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 1)
    tipo = Entry(ventana_vehiculo)
    tipo.grid(row = 7, column = 1)

	#Widget Label y Entry Color
    tk.Label(ventana_vehiculo, text = "Color", font = ("Shanti", 12), bg = bg_color).grid(row = 8, column = 1)
    color = Entry(ventana_vehiculo)
    color.grid(row = 9, column = 1)

	#Widget Label y Entry Número de Puertas
    tk.Label(ventana_vehiculo, text = "Puertas", font = ("Shanti", 12), bg = bg_color).grid(row = 10, column = 1)
    n_puertas = Entry(ventana_vehiculo)
    n_puertas.grid(row = 11, column = 1)

    #Widget Botón Crear
    crear = tk.Button(
        ventana_vehiculo, 
        text= "Crear", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 8, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = insertar_datos
        )
    crear.grid(row = 7, column = 3)

    #Widget Botón Modificar
    modificar = tk.Button(
        ventana_vehiculo, 
        text = "Modificar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = modificar_datos
        )
    modificar.grid(row = 9, column = 3)
    modificar["state"] = "disabled"

    #Widget Botón Eliminar
    eliminar = tk.Button(
        ventana_vehiculo, 
        text = "Eliminar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = eliminar_datos
        )
    eliminar.grid(row = 11, column = 3)
    eliminar["state"] = "disabled"     

    #Widget Botón Inicio
    tk.Label(ventana_vehiculo, text = "", bg = bg_color).grid(row = 12, column = 0)
    tk.Button(
        ventana_vehiculo, 
        text = "Inicio", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 10, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = mostrar_ventana_Inicio
        ).grid(row = 13, column = 0, columnspan = 6)
    tk.Label(ventana_vehiculo, text = "", bg = bg_color).grid(row = 14, column = 0)

    #Mostrar los Datos de la Colección Vehiculo
    mostrar_datos()

def mostrar_ventana_servicio():
    def mostrar_datos():
        global id_ultimo
        id_ultimo = 0
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_servicio.find():
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id_Servicio"]), 
                    values = (documento["Tipo_Lavado"], documento["Tiempo_Min"], documento["Agua_Litros"], documento["Elec_kWh"])
                    )
                id_ultimo = int(documento["id_Servicio"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def insertar_datos():
        if len(tipo_lavado.get()) !=0 and len(tiempo_min.get()) !=0 and len(agua_litros.get()) !=0 and len(elec_kwh.get()) !=0:
            try:
                documento = {
                    "id_Servicio": int(id_ultimo+1), 
                    "Tipo_Lavado": tipo_lavado.get(), 
                    "Tiempo_Min": float(tiempo_min.get()), 
                    "Agua_Litros": float(agua_litros.get()),
                    "Elec_kWh": float(elec_kwh.get())}
                collection_servicio.insert_one(documento)
                tipo_lavado.delete(0,END)
                tiempo_min.delete(0,END)
                agua_litros.delete(0,END)
                elec_kwh.delete(0,END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror(message = "Campos Vacíos")
        mostrar_datos()

    def modificar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        if len(tipo_lavado.get()) !=0 and len(tiempo_min.get()) !=0 and len(agua_litros.get()) !=0 and len(elec_kwh.get()) !=0:
            try:
                idBuscar = {"id_Servicio":id_local}
                nuevosValores = {
                    "$set":{
                        "id_Servicio": int(id_local), 
                        "Tipo_Lavado": tipo_lavado.get(), 
                        "Tiempo_Min": float(tiempo_min.get()), 
                        "Agua_Litros": float(agua_litros.get()),
                        "Elec_kWh": float(elec_kwh.get())}
                        }
                collection_servicio.update_one(idBuscar, nuevosValores)
                tipo_lavado.delete(0,END)
                tiempo_min.delete(0,END)
                agua_litros.delete(0,END)
                elec_kwh.delete(0,END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror("Los Campos no pueden estar Vacíos")
        mostrar_datos()
        crear["state"] = "normal"
        modificar["state"] = "disabled"

    def eliminar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        try:
            idBuscar = {"id_Servicio":id_local}
            collection_servicio.delete_one(idBuscar)
            tipo_lavado.delete(0,END)
            tiempo_min.delete(0,END)
            agua_litros.delete(0,END)
            elec_kwh.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
        crear["state"] = "normal"
        modificar["state"] = "disabled"
        eliminar["state"] = "disabled"
        mostrar_datos()

    def seleccionar_registro(event):
        global id_local, ver_id
        id_local = tabla.item(tabla.selection())["text"]
        documento = collection_servicio.find({"id_Servicio": id_local})[0]
        limpiar_label(ver_id)
        ver_id = Label(ventana_servicio, text = str(id_local), font = ("Shanti", 16), bg = bg_color)
        ver_id.grid(row = 5, column = 0) 
        tipo_lavado.delete(0, END)
        tipo_lavado.insert(0, documento["Tipo_Lavado"])
        tiempo_min.delete(0, END)
        tiempo_min.insert(0, documento["Tiempo_Min"])
        agua_litros.delete(0, END)
        agua_litros.insert(0, documento["Agua_Litros"])
        elec_kwh.delete(0, END)
        elec_kwh.insert(0, documento["Elec_kWh"])
        crear["state"] = "disabled"
        modificar["state"] = "normal"
        eliminar["state"] = "normal"
    
    #Limpiar la ventana y sobreexponer la nueva ventana        
    limpiar_widgets(ventana_inicio)
    ventana_servicio.tkraise()

    #Widget Label Servicio
    tk.Label(
        ventana_servicio, 
        text = "Servicio", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Ubuntu", 18)
        ).grid(row = 0, column = 0, columnspan = 4)

    #Widget Tabla
    tabla = ttk.Treeview(ventana_servicio, columns=4)

    #Definir las columnas de la Tabla
    tabla['columns'] = ("Tipo_Lavado", "Tiempo_Min", "Agua_Litros", "Elec_kWh")
    tabla.column("#0", anchor = "center", width = 70)
    tabla.column("Tipo_Lavado", anchor = "center", width = 120)
    tabla.column("Tiempo_Min", anchor = "center", width = 80)
    tabla.column("Agua_Litros", anchor = "center", width = 80)
    tabla.column("Elec_kWh", anchor = "center", width = 80)

    #Crear Encabezados de la Tabla 
    tabla.heading("#0", text = "Id", anchor = "center")
    tabla.heading("Tipo_Lavado", text = "Tipo de Lavado", anchor = "center")
    tabla.heading("Tiempo_Min", text = "Minutos", anchor = "center")
    tabla.heading("Agua_Litros", text = "Litros", anchor = "center")
    tabla.heading("Elec_kWh", text = "kWh", anchor = "center")
    tabla.grid(row = 2, column = 0, columnspan = 6, sticky = 'nsew')
    tabla.bind("<Double-Button-1>", seleccionar_registro)

    #Widget Scrollbar
    scrollbar = ttk.Scrollbar(ventana_servicio, orient = tk.VERTICAL, command = tabla.yview)
    tabla.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 2, column = 6, sticky = 'ns')

    #Widget Label CRUD
    tk.Label(
        ventana_servicio, 
        text = "CRUD", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Shanti", 20)
        ).grid(row = 3, column = 0, columnspan = 4)

    #Widget Label Id
    tk.Label(ventana_servicio, text = "Id", font = ("Shanti", 12), bg = bg_color).grid(row = 4, column = 0)
    ver_id = tk.Label(ventana_servicio, text = "", font = ("Shanti", 16), bg=bg_color)
    ver_id.grid(row = 5, column = 0)

    #Widget Label y Entry Tipo Lavado
    tk.Label(ventana_servicio, text = "Tipo Lavado", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 0)
    tipo_lavado = Entry(ventana_servicio)
    tipo_lavado.grid(row = 7, column = 0)

    #Widget Label y Entry Tiempo Minutos
    tk.Label(ventana_servicio, text = "Minutos", font = ("Shanti", 12), bg = bg_color).grid(row = 8, column = 0)
    tiempo_min = Entry(ventana_servicio)
    tiempo_min.grid(row = 9, column = 0)

    #Widget Label y Entry Litros Agua
    tk.Label(ventana_servicio, text = "Litros", font = ("Shanti", 12), bg = bg_color).grid(row = 10, column = 0)
    agua_litros = Entry(ventana_servicio)
    agua_litros.grid(row = 11, column = 0)

    #Widget Label y Entry kWh
    tk.Label(ventana_servicio, text = "kWh", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 1)
    elec_kwh = Entry(ventana_servicio)
    elec_kwh.grid(row = 7, column = 1)

    #Widget Botón Crear
    crear = tk.Button(
        ventana_servicio, 
        text= "Crear", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 8, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = insertar_datos
        )
    crear.grid(row = 7, column = 3)

    #Widget Botón Modificar
    modificar = tk.Button(
        ventana_servicio, 
        text = "Modificar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = modificar_datos
        )
    modificar.grid(row = 9, column = 3)
    modificar["state"] = "disabled"

    #Widget Botón Eliminar
    eliminar = tk.Button(
        ventana_servicio, 
        text = "Eliminar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = eliminar_datos
        )
    eliminar.grid(row = 11, column = 3)
    eliminar["state"] = "disabled"     

    #Widget Botón Inicio
    tk.Label(ventana_servicio, text = "", bg=bg_color).grid(row = 12, column = 0)
    tk.Button(
        ventana_servicio, 
        text = "Inicio", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 10, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = mostrar_ventana_Inicio
        ).grid(row = 13, column = 0, columnspan = 6)
    tk.Label(ventana_servicio, text = "", bg = bg_color).grid(row = 14, column = 0)

    #Mostrar los Datos de la Colección Servicio
    mostrar_datos()

def mostrar_ventana_establecimiento():
    def mostrar_datos():
        global id_ultimo
        id_ultimo = 0
        try:
            registros = tabla.get_children()
            for registro in registros:
                tabla.delete(registro)
            for documento in collection_establecimiento.find():
                tabla.insert(
                    parent = '', 
                    index = "end", 
                    text = int(documento["id_Establecimiento"]), 
                    values = (documento["Provincia"], documento["Fecha"], documento["Ingreso_Total"])
                    )
                id_ultimo = int(documento["id_Establecimiento"])
                client.close()
        except pymongo.errors.ServerSelectionTimeoutError as errorTiempo:
            print("Tiempo Excedido "+errorTiempo)
        except pymongo.errors.ConnectionFailure as error:
            print("Fallo de Conexión con la Base de Datos "+error)
        except KeyError:
            None

    def insertar_datos():
        if len(provincia.get()) != 0 and len(fecha.get()) != 0 and len(ingreso_total.get()) != 0:
            try:
                documento = {
                    "id_Establecimiento": int(id_ultimo+1), 
                    "Provincia": provincia.get(), 
                    "Fecha": fecha.get(), 
                    "Ingreso_Total": float(ingreso_total.get())}
                collection_establecimiento.insert_one(documento)
                provincia.delete(0, END)
                fecha.delete(0, END)
                ingreso_total.delete(0, END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror(message = "Campos Vacíos")
        mostrar_datos()

    def modificar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        if len(provincia.get()) !=0 and len(fecha.get()) !=0 and len(ingreso_total.get()) !=0:
            try:
                idBuscar = {"id_Establecimiento":id_local}
                nuevosValores = {
                    "$set":{
                        "id_Establecimiento": int(id_local), 
                        "Provincia": provincia.get(), 
                        "Fecha": fecha.get(), 
                        "Ingreso_Total": float(ingreso_total.get())}
                        }
                collection_establecimiento.update_one(idBuscar, nuevosValores)
                provincia.delete(0,END)
                fecha.delete(0,END)
                ingreso_total.delete(0,END)
            except pymongo.errors.ConnectionFailure as error:
                print(error)
        else:
            messagebox.showerror("Los Campos no pueden estar Vacíos")
        mostrar_datos()
        crear["state"] = "normal"
        modificar["state"] = "disabled"

    def eliminar_datos():
        global id_local, ver_id
        limpiar_label(ver_id)
        try:
            idBuscar = {"id_Establecimiento":id_local}
            collection_establecimiento.delete_one(idBuscar)
            provincia.delete(0,END)
            fecha.delete(0,END)
            ingreso_total.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
        crear["state"] = "normal"
        modificar["state"] = "disabled"
        eliminar["state"] = "disabled"
        mostrar_datos()

    def seleccionar_registro(event):
        global id_local, ver_id
        id_local = tabla.item(tabla.selection())["text"]
        documento = collection_establecimiento.find({"id_Establecimiento": id_local})[0]
        limpiar_label(ver_id)
        ver_id = Label(ventana_establecimiento, text = str(id_local), font = ("Shanti", 16), bg = bg_color)
        ver_id.grid(row = 5, column = 0) 
        provincia.delete(0, END)
        provincia.insert(0, documento["Provincia"])
        fecha.delete(0, END)
        fecha.insert(0, documento["Fecha"])
        ingreso_total.delete(0, END)
        ingreso_total.insert(0, documento["Ingreso_Total"])
        crear["state"] = "disabled"
        modificar["state"] = "normal"
        eliminar["state"] = "normal"
    
    #Limpiar la ventana y sobreexponer la nueva ventana        
    limpiar_widgets(ventana_inicio)
    ventana_establecimiento.tkraise()

    #Widget Label Establecimiento
    tk.Label(
        ventana_establecimiento, 
        text = "Establecimiento", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Ubuntu", 18)
        ).grid(row = 0, column = 0, columnspan = 4)

    #Widget Tabla
    tabla = ttk.Treeview(ventana_establecimiento, columns=4)

    #Definir las columnas de la Tabla
    tabla['columns'] = ("Provincia", "Fecha", "Ingreso_Total")
    tabla.column("#0", anchor = "center", width = 70)
    tabla.column("Provincia", anchor = "center", width = 200)
    tabla.column("Fecha", anchor = "center", width = 120)
    tabla.column("Ingreso_Total", anchor = "center", width = 120)

    #Crear Encabezados de la Tabla 
    tabla.heading("#0", text = "Id", anchor = "center")
    tabla.heading("Provincia", text = "Provincia", anchor = "center")
    tabla.heading("Fecha", text = "Fecha", anchor = "center")
    tabla.heading("Ingreso_Total", text = "Ingreso Total", anchor = "center")
    tabla.grid(row = 2, column = 0, columnspan = 4, sticky = 'nsew')
    tabla.bind("<Double-Button-1>", seleccionar_registro)

    #Widget Scrollbar
    scrollbar = ttk.Scrollbar(ventana_establecimiento, orient = tk.VERTICAL, command = tabla.yview)
    tabla.configure(yscroll = scrollbar.set)
    scrollbar.grid(row = 2, column = 5, sticky = 'ns')

    #Widget Label CRUD
    tk.Label(
        ventana_establecimiento, 
        text = "CRUD", 
        bg = bg_color, fg = "#0a2f55", 
        font = ("Shanti", 20)
        ).grid(row = 3, column = 0, columnspan = 4)

    #Widget Label Id
    tk.Label(ventana_establecimiento, text = "Id", font = ("Shanti", 12), bg = bg_color).grid(row = 4, column = 0)
    ver_id = tk.Label(ventana_establecimiento, text = "", font = ("Shanti", 16), bg=bg_color)
    ver_id.grid(row = 5, column = 0)

    #Widget Label y Entry Provincia
    tk.Label(ventana_establecimiento, text = "Provincia", font = ("Shanti", 12), bg = bg_color).grid(row = 6, column = 0)
    provincia = Entry(ventana_establecimiento)
    provincia.grid(row = 7, column = 0)

    #Widget Label y Entry Fecha
    tk.Label(ventana_establecimiento, text = "Fecha", font = ("Shanti", 12), bg = bg_color).grid(row = 8, column = 0)
    fecha = Entry(ventana_establecimiento)
    fecha.grid(row = 9, column = 0)

    #Widget Label y Entry Ingreso Total
    tk.Label(ventana_establecimiento, text = "Ingreso Total", font = ("Shanti", 12), bg = bg_color).grid(row = 10, column = 0)
    ingreso_total = Entry(ventana_establecimiento)
    ingreso_total.grid(row = 11, column = 0)

    #Widget Botón Crear
    crear = tk.Button(
        ventana_establecimiento, 
        text= "Crear", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 8, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = insertar_datos
        )
    crear.grid(row = 7, column = 3)

    #Widget Botón Modificar
    modificar = tk.Button(
        ventana_establecimiento, 
        text = "Modificar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = modificar_datos
        )
    modificar.grid(row = 9, column = 3)
    modificar["state"] = "disabled"

    #Widget Botón Eliminar
    eliminar = tk.Button(
        ventana_establecimiento, 
        text = "Eliminar", font = ("Shanti", 14),
        width = 8, 
        bg = "#0a2f55", fg = "white", 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = eliminar_datos
        )
    eliminar.grid(row = 11, column = 3)
    eliminar["state"] = "disabled"     

    #Widget Botón Inicio
    tk.Label(ventana_establecimiento, text = "", bg=bg_color).grid(row = 12, column = 0)
    tk.Button(
        ventana_establecimiento, 
        text = "Inicio", font = ("Shanti", 14), 
        bg = "#0a2f55", fg = "white",
        width = 10, 
        cursor = "hand2", 
        activebackground = "#00a4c5", activeforeground = "#0a2f55",
        command = mostrar_ventana_Inicio
        ).grid(row = 13, column = 0, columnspan = 4)
    tk.Label(ventana_establecimiento, text = "", bg = bg_color).grid(row = 14, column = 0)

    #Mostrar los Datos de la Colección Establecimiento
    mostrar_datos()
    
inicio = Tk()
inicio.title("LavaCar")
inicio.eval("tk::PlaceWindow . center")
inicio.columnconfigure(0, weight = 1)
inicio.rowconfigure(0, weight = 1)
inicio.attributes('-fullscreen', True)

#Widget Menu
menu_inicio = Menu(inicio)
inicio.config(menu = menu_inicio)
lavacar_menu = Menu(menu_inicio)
menu_inicio.add_cascade(label = "Menu", menu = lavacar_menu)
lavacar_menu.add_command(label = "Inicio", command = mostrar_ventana_Inicio)
lavacar_menu.add_command(label = "Cliente", command = mostrar_ventana_cliente)
lavacar_menu.add_command(label = "Vehiculo", command = mostrar_ventana_vehiculo)
lavacar_menu.add_command(label = "Servicio", command = mostrar_ventana_servicio)
lavacar_menu.add_command(label = "Establecimiento", command = mostrar_ventana_establecimiento)
lavacar_menu.add_command(label = "Salir", command = exit)

bg_color = "#cecece"
pyglet.font.add_file("fonts/Ubuntu-Bold.ttf")
pyglet.font.add_file("fonts/Shanti-Regular.ttf")
pyglet.font.add_file("fonts/Play-Bold.ttf")

#Declarando, Inicializando y Mostrando Ventana de Inicio
ventana_inicio = tk.Frame(inicio, bg = bg_color)
ventana_cliente = tk.Frame(inicio, bg = bg_color)
ventana_vehiculo = tk.Frame(inicio, bg = bg_color)
ventana_servicio = tk.Frame(inicio, bg = bg_color)
ventana_establecimiento = tk.Frame(inicio, bg = bg_color)
for ventana in (ventana_inicio, ventana_cliente, ventana_vehiculo, ventana_servicio, ventana_establecimiento):
    ventana.grid(row = 0, column = 0, sticky = "nesw")
    ventana.columnconfigure(0, weight = 1)
    ventana.columnconfigure(1, weight = 1)
    ventana.columnconfigure(2, weight = 1)
    ventana.columnconfigure(3, weight = 1)
    ventana.rowconfigure(0, weight = 1)
    ventana.rowconfigure(1, weight = 1)
    ventana.rowconfigure(2, weight = 1)
    ventana.rowconfigure(3, weight = 1)

mostrar_ventana_Inicio()

#Iniciar el Programa
inicio.mainloop()