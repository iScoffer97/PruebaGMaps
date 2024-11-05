from conexion import Conexion
from cliente import Cliente

class ClienteDAO:

    _SELECCIONAR = 'SELECT * FROM zonafit'
    _INSERTAR = 'INSERT INTO zonafit(nombre, apellido, membresia) VALUES(%s, %s, %s)'
    _ACTUALIZAR = 'UPDATE zonafit SET nombre=%s, apellido=%s, membresia=%s WHERE id=%s'
    _ELIMINAR = 'DELETE FROM zonafit WHERE id=%s'


    @classmethod
    def seleccionar(cls):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute(cls._SELECCIONAR)
            registros = cursor.fetchall()
            # Mapeo de clase-tabla cliente
            clientes = []
            for registro in registros:
                cliente = Cliente(registro[0], registro[1], registro[2], registro[3])
                clientes.append(cliente)
            return clientes
        except Exception as e:
            print(f'Ocurrió un error al seleccionar clientes: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def insertar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.nombre, cliente.apellido, cliente.membresia)
            cursor.execute(cls._INSERTAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrió un Error: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def eliminar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.id,)
            cursor.execute(cls._ELIMINAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrió un error a la hora de eliminar un registro: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)

    @classmethod
    def actualizar(cls, cliente):
        conexion = None
        try:
            conexion = Conexion.obtener_conexion()
            cursor = conexion.cursor()
            valores = (cliente.nombre, cliente.apellido, cliente.membresia, cliente.id)
            cursor.execute(cls._ACTUALIZAR, valores)
            conexion.commit()
            return cursor.rowcount
        except Exception as e:
            print(f'Ocurrió una excepción: {e}')
        finally:
            if conexion is not None:
                cursor.close()
                Conexion.liberar_conexion(conexion)


if __name__ == '__main__':
    # Insertar
    #cliente1 = Cliente(nombre='Juan', apellido='Garcia', membresia=123456)
    #clientes_insertados = ClienteDAO.insertar(cliente1)
    #print(f'Clientes insertados: {clientes_insertados}')

    # Actualizar
    #cliente1 = Cliente(nombre='Ingrid', apellido='Borràs', membresia=9876, id=7)
    #clientes_actualizados = ClienteDAO.actualizar(cliente1)
    #print(f'Clientes actualizados: {clientes_actualizados}')

    # Eliminar
    cliente_eliminado = Cliente(id=6)
    clientes_eliminados = ClienteDAO.eliminar(cliente_eliminado)
    print(f'Clientes eliminados: {clientes_eliminados}')

    #Seleccionar
    clientes = ClienteDAO.seleccionar()
    for cliente in clientes:
        print(cliente)
