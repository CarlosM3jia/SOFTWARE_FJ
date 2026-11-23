
from abc import ABC, abstractmethod


class Entidad(ABC):
    """
    Clase abstracta que representa una entidad general
    dentro del sistema Software FJ.
    """

    def __init__(self, identificacion):
        if identificacion is None or not str(identificacion).strip():
            raise ValueError(
                "La identificación de la entidad es obligatoria."
            )

        self.__identificacion = str(identificacion).strip()

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

