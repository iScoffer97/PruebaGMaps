from cliente import Cliente
from cliente_dao import ClienteDAO
from conexion import Conexion

print('*** Clientes de ZonaFit ***')
opcion = None
while opcion != 5:
    print('''Menú:
    1. Listar clientes
    2. Agregar cliente
    3. Modificar cliente
    4. Eliminar cliente
    5. Salir    
    ''')
    opcion = int(input('Que opción escoges del menú: '))

    if opcion == 1:
        # Listar clientes
        clientes = ClienteDAO.seleccionar()
        print('\n*** Listado de clientes ***')
        for cliente in clientes:
            print(cliente)
        print()
    elif opcion == 2:
        # Agregar cliente
        nombre_var = input('Escribe el nombre: ')
        apellido_var = input('Escribe el apellido: ')
        membresia_var = input('Escribe la membresia: ')
        cliente = Cliente(nombre=nombre_var, apellido=apellido_var, membresia=membresia_var)
        clientes_insertados = ClienteDAO.insertar(cliente)
        print(f'Clientes insertados: {clientes_insertados}')
    elif opcion == 3:
        # Modificar cliente
        id_cliente_var = int(input('Escribe el ID del cliente a modificar: '))
        nombre_var = input('Escribe el nuevo nombre: ')
        apellido_var = input('Escribe el nuevo apellido: ')
        membresia_var = input('Escribe la nueva membresia: ')
        cliente = Cliente(id_cliente_var, nombre_var, apellido_var, membresia_var)
        clientes_actualizados = ClienteDAO.actualizar(cliente)
        print(f'Clientes actualizados: {clientes_actualizados}')
    elif opcion == 4:
        id_cliente_var = int(input('Escribe el ID del cliente a eliminar: '))
        cliente = Cliente(id=id_cliente_var)
        clientes_eliminados = ClienteDAO.eliminar(cliente)
        print(f'Clientes eliminados: {clientes_eliminados}')
else:
    print(f'Salimos de la aplicación...')