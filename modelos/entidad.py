
from abc import ABC, abstractmethod
from excepciones.excepciones_clientes import DatosClienteInvalidos


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general
    dentro del sistema Software FJ.
    """

    def __init__(self, identificacion):
        self.__identificacion = identificacion

    @property
    def identificacion(self):
        """Permite consultar la identificación."""
        return self.__identificacion

    @abstractmethod
    def obtener_descripcion(self):
        """
        Método abstracto que deben implementar
        las clases que hereden de Entidad.
        """
        pass
