#Requerimientos

1. Control de Acceso
        El sistema tendrá control de acceso y solamente los usuarios autorizados podrán ingresar. 
        Los usuarios deben registrarse al sistema con un correo electrónico, nombre de usuario y contraseña.
        El nombre de usuario será único y no podrá registrarse más de una persona con el mismo nombre de usuario.
        Para autorizarse se tendrá una página de inicio de sesión y el registro se hará en una página independiente.
       
2. Administración de Entidades y Datos
        Se tendrán páginas con las mismas funciones para las entidades Cliente, Vehiculo, Servicio y Establecimiento.
        Cada entidad será independiente una de la otra y los datos solicitados serán dependientes de la entidad.
        Habrán casillas de texto y botones para ingresar la información.
        Se gestionarán los datos del LavaCar mediante las funciones básicas CRUD (Create, Read, Update y Delete).
        Para localizar los registros, se utilizará una llave primaria única.

3. Verificación de Datos
        Todos los datos que se ingresen al sistema, deberán verificarse de forma tal que no se registren datos nulos
        o los mismos no correspondan al tipo de dato solicitado.

4. Visualización de Datos Importantes
        Mediante una página de Lobby/Inicio se mostrarán y actualizarán automáticamente los principales datos del LavaCar.

5. Navegación del Sistema
        Implementación de un Menú en todas las páginas para la navegación del sistema.

6. Registro de Facturación
        En un apartado se llevarán los datos de facturación. Será necesario implementar una herramienta para imprimir las facturas.
        Cada facturación tendrá un dato único para la posible localización.
        

#Dependencias
MongoDB
Python3+
    Librerias
        tkinter
Conda
    Librerias
        pymongo
        pylint
        pillow
        piglet
        dnspython

#Referencias
tkinter
    https://docs.python.org/3/library/tk.html
pymongo
    https://pymongo.readthedocs.io/en/stable/tutorial.html
Treeview
    https://tkdocs.com/tutorial/tree.html
        