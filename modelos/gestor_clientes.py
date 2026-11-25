
from modelos.cliente import Cliente
from excepciones.excepciones_clientes import (
    ClienteNoEncontrado,
    ErrorCliente
)


class GestorClientes:
    """
    Administra el registro, búsqueda, actualización,
    eliminación y consulta de clientes.
    """

    def __init__(self):
        # Diccionario para almacenar clientes en memoria.
        self.__clientes = {}

    def registrar_cliente(self, cliente):
        """Registra un nuevo cliente."""
        if not isinstance(cliente, Cliente):
            raise TypeError("El objeto debe ser un cliente válido.")

        identificacion = str(cliente.identificacion).strip()

        if not identificacion:
            raise ValueError("La identificación del cliente es obligatoria.")

        if identificacion in self.__clientes:
            raise ErrorCliente(
                f"Ya existe un cliente con identificación {identificacion}."
            )

        self.__clientes[identificacion] = cliente

        return "Cliente registrado correctamente."

    def buscar_cliente(self, identificacion):
        """Busca un cliente por su identificación."""
        identificacion = str(identificacion).strip()

        if identificacion not in self.__clientes:
            raise ClienteNoEncontrado(
                f"No se encontró el cliente {identificacion}."
            )

        return self.__clientes[identificacion]

    def actualizar_cliente(
        self, identificacion, nombre=None, correo=None, telefono=None
    ):
        """Actualiza los datos de un cliente existente."""
        cliente = self.buscar_cliente(identificacion)

        return cliente.actualizar_datos(
            nombre=nombre,
            correo=correo,
            telefono=telefono
        )

    def eliminar_cliente(self, identificacion):
        """Elimina un cliente del sistema."""
        cliente = self.buscar_cliente(identificacion)

        del self.__clientes[str(identificacion).strip()]

        return f"Cliente {cliente.nombre} eliminado correctamente."

    def listar_clientes(self):
        """Devuelve la lista de clientes registrados."""
        return list(self.__clientes.values())

    def cantidad_clientes(self):
        """Devuelve el número de clientes registrados."""
        return len(self.__clientes)
