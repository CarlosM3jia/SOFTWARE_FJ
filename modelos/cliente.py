
import re

from modelos.entidad import Entidad
from excepciones.excepciones_clientes import DatosClienteInvalidos


class Cliente(Entidad):
    """
    Representa un cliente registrado en Software FJ.
    Hereda de la clase abstracta Entidad.
    """

    def __init__(self, identificacion, nombre, correo, telefono):
        super().__init__(identificacion)

        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatosClienteInvalidos(
                "El nombre debe tener al menos 3 caracteres."
            )

        self.__nombre = valor.strip().title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str):
            raise DatosClienteInvalidos("El correo debe ser texto.")

        valor = valor.strip().lower()

        patron = r"^[\w.+-]+@[\w-]+\.[\w.-]+$"

        if not re.match(patron, valor):
            raise DatosClienteInvalidos(
                "El correo electrónico no es válido."
            )

        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str):
            raise DatosClienteInvalidos("El teléfono debe ser texto.")

        valor = valor.strip()

        if not valor.isdigit() or not 7 <= len(valor) <= 15:
            raise DatosClienteInvalidos(
                "El teléfono debe contener entre 7 y 15 dígitos."
            )

        self.__telefono = valor

    def obtener_descripcion(self):
        return (
            f"Cliente: {self.nombre} | "
            f"Identificación: {self.identificacion} | "
            f"Correo: {self.correo} | "
            f"Teléfono: {self.telefono}"
        )

    def actualizar_datos(self, nombre=None, correo=None, telefono=None):
        """
        Permite actualizar uno o varios datos del cliente.
        Solo modifica los campos que reciben un nuevo valor.
        """

        if nombre is not None:
            self.nombre = nombre

        if correo is not None:
            self.correo = correo

        if telefono is not None:
            self.telefono = telefono

        return "Datos del cliente actualizados correctamente."

