from mysql.connector import pooling
from mysql.connector import Error
import sys

class Conexion:
    _DATABASE = 'zona_fit_db'
    _USERNAME = 'root'
    _PASSWORD = 'amorales'
    _DB_PORT = '3306'
    _HOST = 'localhost'
    _POOL_SIZE = 5
    _POOL_NAME = 'zona_fit_pool'
    _pool = None

    @classmethod
    def obtener_pool(cls):
        if cls._pool is None: #Creamos el objeto pool
            try:
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name=cls._POOL_NAME,
                    pool_size=cls._POOL_SIZE,
                    host=cls._HOST,
                    port=cls._DB_PORT,
                    database=cls._DATABASE,
                    user=cls._USERNAME,
                    password=cls._PASSWORD
                )
                print('Conexión establecida correctamente')
                return cls._pool
            except Error as e:
                print(f'Ha ocurrido un error al obtener el pool {e}')
        else:
            return cls._pool

    @classmethod
    def obtener_conexion(cls):
        return cls.obtener_pool().get_connection()

    @classmethod
    def liberar_conexion(cls , conexion):
        conexion.close()
        print('Conexión devuelta al pool.')


if __name__ == '__main__':
    #pool = Conexion.obtener_pool()
    #print(pool)
    conexion1 = Conexion.obtener_conexion()
    print(conexion1)
    Conexion.liberar_conexion(conexion1)
