import tkinter as tk
from tkinter import ttk, messagebox

from cliente import Cliente
from cliente_dao import ClienteDAO


class ZonaFitGUI(tk.Tk):
    COLOR_VENTANA = '#1d2d44'
    def __init__(self):
        super().__init__()
        self.id_cliente = None
        # Configuración de ventana
        self.configurar_ventana()
        # Configuración del grid
        self.configurar_grid()
        # Mostrar el formulario para introducir clientes
        self.formulario_clientes()
        # Introducimos el título principal
        self.titulo_principal()
        # Mostramos la tabla
        self.cargar_tabla()
        # Botones del formulario
        self.mostrar_botones()



    def configurar_ventana(self):
        self.geometry('900x600')
        self.title('ZonaFit (GYM)')
        self.configure(background=self.COLOR_VENTANA)
        # Aplicamos el estilo
        self.estilos = ttk.Style()
        self.estilos.theme_use('clam') # Preparamos para el modo oscuro
        self.estilos.configure(self, background=self.COLOR_VENTANA,
                               foreground='white',
                               fieldbackground='black')

    def configurar_grid(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        # self.rowconfigure(0, weight=1)
        # self.rowconfigure(1, weight=7)
        # self.rowconfigure(2, weight=4)

    def titulo_principal(self):
        titulo1 = ttk.Label(self, text='Zona Fit (GYM)', background=self.COLOR_VENTANA, foreground='white', font=('Arial', 22), anchor=tk.CENTER)
        titulo1.grid(row=0, column=0, columnspan=2, pady=30)

    def formulario_clientes(self):
        self.frame_forma = ttk.Frame()
        # Nombre
        nombre_l = ttk.Label(self.frame_forma, text='Nombre: ')
        nombre_l.grid(row=0, column=0, sticky=tk.W, pady=20, padx=5)
        self.nombre_t = ttk.Entry(self.frame_forma)
        self.nombre_t.grid(row=0, column=1)
        # Apellido
        apellido_l = ttk.Label(self.frame_forma, text='Apellido: ')
        apellido_l.grid(row=1, column=0, sticky=tk.W, pady=20, padx=5)
        self.apellido_t = ttk.Entry(self.frame_forma)
        self.apellido_t.grid(row=1, column=1)
        # Membresía
        membresia_l = ttk.Label(self.frame_forma, text='Membresía: ')
        membresia_l.grid(row=2, column=0, sticky=tk.W, pady=20, padx=5)
        self.membresia_t = ttk.Entry(self.frame_forma)
        self.membresia_t.grid(row=2, column=1)

        # Publicar el frame de forma
        self.frame_forma.grid(row=1, column=0)

    def cargar_tabla(self):
        self.frame_tabla = ttk.Frame(self)
        # Definimos los estilos de la tabla
        self.estilos.configure('Treeview', background='black',
                               foreground='white',
                               fieldbackground='black',
                               rowheight=20)
        # Definimos las columnas
        columnas = ('ID', 'Nombre', 'Apellido', 'Membresia')
        # Creamos objeto tabla
        self.tabla = ttk.Treeview(self.frame_tabla, columns=columnas, show='headings')
        # Agregamos los headings
        self.tabla.heading('ID', text='ID', anchor=tk.CENTER)
        self.tabla.heading('Nombre', text='Nombre', anchor=tk.W)
        self.tabla.heading('Apellido', text='Apellido', anchor=tk.W)
        self.tabla.heading('Membresia', text='Membresía', anchor=tk.W)
        # Definir las columnas
        self.tabla.column('ID', anchor=tk.CENTER, width=50)
        self.tabla.column('Nombre', anchor=tk.W, width=100)
        self.tabla.column('Apellido', anchor=tk.W, width=100)
        self.tabla.column('Membresia', anchor=tk.W, width=100)
        # Cargar los datos de la BBDD
        clientes = ClienteDAO.seleccionar()
        for cliente in clientes:
            self.tabla.insert(parent='', index=tk.END, values=(cliente.id, cliente.nombre, cliente.apellido, cliente.membresia))

        # Agregamos Scrollbar
        scrollbar = ttk.Scrollbar(self.frame_tabla, orient=tk.VERTICAL,
                                  command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # Asociar el evento select
        self.tabla.bind('<<TreeviewSelect>>', self.cargar_cliente)

        # Publicamos la tabla
        self.tabla.grid(row=0, column=0)
        # Mostramos el frame de table
        self.frame_tabla.grid(row=1, column=1, padx=20)

    def mostrar_botones(self):
        self.frame_botones = ttk.Frame()
        # Crear los botones
        # Botón de agregar
        agregar_boton = ttk.Button(self.frame_botones, text='Guardar',
                                   command=self.validar_cliente)
        agregar_boton.grid(row=0, column=0, padx=30)
        # Botón de eliminar
        eliminar_boton = ttk.Button(self.frame_botones, text='Eliminar',
                                   command=self.eliminar_cliente)
        eliminar_boton.grid(row=0, column=1, padx=30)
        # Botón de limpiar
        limpiar_boton = ttk.Button(self.frame_botones, text='Limpiar',
                                   command=self.limpiar_datos)
        limpiar_boton.grid(row=0, column=2, padx=30)

        # Aplicar estilo a los botones
        self.estilos.configure('TButton', background='#005f73')
        self.estilos.map('TButton', background=[('active', '#0a9396')])

        # Publicamos frame botones
        self.frame_botones.grid(row=2, column=0, columnspan=2, pady=20)

    def validar_cliente(self):
        # Validar los campos
        if (self.nombre_t.get() and self.apellido_t.get() and self.membresia_t.get()):
            if self.validar_membresia():
                self.guardar_cliente()
            else:
                messagebox.showerror(title='Atención', message='El valor de membresía no es numérico')
                self.membresia_t.delete(0, tk.END)
                self.membresia_t.focus_set()
        else:
            messagebox.showerror(title='Atención', message='Debe llenar el formulario')
            self.nombre_t.focus_set()

    def validar_membresia(self):
        try:
            int(self.membresia_t.get())
            return True
        except:
            return False

    def guardar_cliente(self):
        # Recuperar los valores de las cajas de texto
        nombre = self.nombre_t.get()
        apellido = self.apellido_t.get()
        membresia = self.membresia_t.get()
        # Validamso el valor de id_cliente
        if self.id_cliente is None:
            cliente = Cliente(nombre=nombre, apellido=apellido, membresia=membresia)
            ClienteDAO.insertar(cliente)
            messagebox.showinfo(title='Agregar', message='Cliente agregado...')
        else: # Actualizar registro
            cliente = Cliente(self.id_cliente, nombre, apellido, membresia)
            ClienteDAO.actualizar(cliente)
            messagebox.showinfo(title='Actualizar', message='Cliente actualizado')
        # Volvemos a mostrar los datos y limpiamos el formulario
        self.recargar_datos()

    def recargar_datos(self):
        # Se vuelve a cargar los datos de la tabla
        self.cargar_tabla()
        # Limpiar los datos
        self.limpiar_datos()

    def limpiar_datos(self):
        self.limpiar_formulario()
        self.id_cliente = None

    def limpiar_formulario(self):
        self.nombre_t.delete(0, tk.END)
        self.apellido_t.delete(0, tk.END)
        self.membresia_t.delete(0, tk.END)

    def eliminar_cliente(self):
        if self.id_cliente is None:
            messagebox.showerror(title='Atención', message='Debes seleccionar un cliente a eliminar')
        else:
            cliente = Cliente(self.id_cliente)
            ClienteDAO.eliminar(cliente)
            messagebox.showinfo(title='Eliminado', message='Cliente eliminado')
            self.recargar_datos()


    def limpiar_cliente(self):
        pass

    def cargar_cliente(self, event):
        elemento_seleccionado = self.tabla.selection()[0]
        elemento = self.tabla.item(elemento_seleccionado)
        cliente_t = elemento['values'] # Tupla de valores del cliente seleccionado
        # Recuperar valor de cada cliente
        self.id_cliente = cliente_t[0]
        nombre = cliente_t[1]
        apellido = cliente_t[2]
        membresia = cliente_t[3]
        # Antes de cargar, limpiamos el formulario
        self.limpiar_formulario()
        # Cargamos los valores
        self.nombre_t.insert(0, nombre)
        self.apellido_t.insert(1, apellido)
        self.membresia_t.insert(2, membresia)


if __name__ == '__main__':
    ventana = ZonaFitGUI()
    ventana.mainloop()