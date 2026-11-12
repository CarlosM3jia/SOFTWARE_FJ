from abc import ABC, abstractmethod

# ==========================================
# CLASE ABSTRACTA BASE: Servicio
# ==========================================
class Servicio(ABC):
    """
    Clase abstracta que define la estructura común para todos los servicios
    ofrecidos por Software FJ (Abstracción y Polimorfismo).
    """
    def __init__(self, codigo, nombre_servicio, tarifa_base):
        if not codigo or str(codigo).strip() == "":
            raise ValueError("El código del servicio no puede estar vacío.")
        if float(tarifa_base) <= 0:
            raise ValueError("La tarifa base debe ser mayor a cero.")
            
        self._codigo = str(codigo).strip()
        self._nombre_servicio = nombre_servicio
        self._tarifa_base = float(tarifa_base)

    @abstractmethod
    def calcular_costo(self, *args, **kwargs):
        """Método abstracto que será sobrescrito por cada clase hija."""
        pass

    @abstractmethod
    def obtener_descripcion(self):
        """Método abstracto para retornar los detalles del servicio."""
        pass

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre_servicio(self):
        return self._nombre_servicio


# ==========================================
# CLASE HIJA 1: ReservaSala
# ==========================================
class ReservaSala(Servicio):
    def __init__(self, codigo, tarifa_base, capacidad):
        super().__init__(codigo, "Reserva de Sala", tarifa_base)
        if int(capacidad) <= 0:
            raise ValueError("La capacidad de la sala debe ser mayor a cero.")
        self._capacidad = int(capacidad)

    # Sobrecarga de método mediante parámetros opcionales (descuento e impuesto)
    def calcular_costo(self, horas, descuento_porcentaje=0.0, impuesto=0.19):
        if horas <= 0:
            raise ValueError("Las horas de reserva de sala deben ser mayores a cero.")
        if descuento_porcentaje < 0 or descuento_porcentaje > 100:
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
            
        subtotal = self._tarifa_base * horas
        descuento = subtotal * (descuento_porcentaje / 100)
        total = (subtotal - descuento) * (1 + impuesto)
        return round(total, 2)

    def obtener_descripcion(self):
        return f"[Sala] Código: {self._codigo} | Capacidad: {self._capacidad} personas | Tarifa Base/h: ${self._tarifa_base}"

# ==========================================
# CLASE HIJA 2: AlquilerEquipos
# ==========================================
class AlquilerEquipos(Servicio):
    def __init__(self, codigo, tarifa_base, tipo_equipo):
        super().__init__(codigo, "Alquiler de Equipos", tarifa_base)
        if not tipo_equipo or str(tipo_equipo).strip() == "":
            raise ValueError("Debe especificar el tipo de equipo.")
        self._tipo_equipo = str(tipo_equipo).strip()

    # Sobrecarga de método mediante parámetro opcional (seguro)
    def calcular_costo(self, dias, seguro=0.0):
        if dias <= 0:
            raise ValueError("Los días de alquiler deben ser mayores a cero.")
        if seguro < 0:
            raise ValueError("El valor del seguro no puede ser negativo.")
            
        total = (self._tarifa_base * dias) + seguro
        return round(total, 2)

    def obtener_descripcion(self):
        return f"[Equipo] Código: {self._codigo} | Tipo: {self._tipo_equipo} | Tarifa Base/día: ${self._tarifa_base}"


# ==========================================
# CLASE HIJA 3: AsesoriaEspecializada
# ==========================================
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo, tarifa_base, area):
        super().__init__(codigo, "Asesoría Especializada", tarifa_base)
        if not area or str(area).strip() == "":
            raise ValueError("Debe especificar el área de la asesoría.")
        self._area = str(area).strip()

    # Sobrecarga de método mediante parámetro opcional (bono de descuento)
    def calcular_costo(self, sesiones, bono_especial=0.0):
        if sesiones <= 0:
            raise ValueError("El número de sesiones debe ser mayor a cero.")
        if bono_especial < 0:
            raise ValueError("El bono especial no puede ser negativo.")
            
        total = (self._tarifa_base * sesiones) - bono_especial
        return max(0.0, round(total, 2))

    def obtener_descripcion(self):
        return f"[Asesoría] Código: {self._codigo} | Área: {self._area} | Tarifa Base/sesión: ${self._tarifa_base}"
    