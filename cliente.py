class Cliente:
    def __init__(self, id=None, nombre=None, apellido=None, membresia=None):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.membresia = membresia

    def __str__(self):
        return f'ID: {self.id}, Nombre: {self.nombre}, Apellido: {self.apellido}, Membresía: {self.membresia}'


if __name__ == '__main__':
    cliente1 = Cliente(8, 'Alejandro', 'Morales', 12345)
    print(cliente1)
