from datetime import datetime  # Fecha de creación de la reserva

from utilidades.logger import registrar_evento, registrar_error  # Log único del sistema


class ReservaError(Exception):
    """Excepción base personalizada para el módulo de reservas."""
    pass


class ReservaNoValidaError(ReservaError):
    """Excepción lanzada cuando los datos de la reserva son incorrectos."""
    pass


class Reserva:
    """
    Clase que representa una reserva en el sistema Software FJ.
    Integra un objeto Cliente y un objeto Servicio (Polimorfismo).
    """
    def __init__(self, id_reserva, cliente, servicio, cantidad):
        self.id_reserva = str(id_reserva).strip()
        self.cliente = cliente
        self.servicio = servicio

        try:  # AJUSTE: la cantidad debe ser numérica (evita un TypeError sin controlar)
            cantidad = float(cantidad)
        except (TypeError, ValueError) as e:
            # AJUSTE: encadenamiento de excepciones con "from"
            raise ReservaNoValidaError("La cantidad debe ser un número.") from e

        if cantidad <= 0:
            raise ReservaNoValidaError("La cantidad (horas/días/sesiones) debe ser mayor a cero.")

        self.cantidad = cantidad
        self.estado = "Pendiente"  # Estados posibles: Pendiente, Confirmada, Cancelada
        self.fecha_creacion = datetime.now()

    def registrar_log(self, mensaje, es_error=False):
        """AJUSTE: escribe en el log único del sistema (logs/software_fj.log)."""
        texto = f"RESERVA {self.id_reserva}: {mensaje}"
        if es_error:
            registrar_error(texto)
        else:
            registrar_evento(texto)

    def confirmar_reserva(self):
        try:
            if self.estado == "Confirmada":
                raise ReservaError(f"La reserva {self.id_reserva} ya se encontraba confirmada previamente.")
            if self.estado == "Cancelada":
                raise ReservaError("No se puede confirmar una reserva que ya fue cancelada.")

            self.estado = "Confirmada"
            msg = f"Reserva confirmada con éxito para el cliente {self.cliente.nombre}."
            print(f"[EXITO] {msg}")
            self.registrar_log(msg)
        except ReservaError as e:
            error_msg = f"Error al intentar confirmar: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg, es_error=True)
            raise
        finally:
            print(f"-> Proceso de confirmación finalizado para la reserva {self.id_reserva}.\n")

    def cancelar_reserva(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaError(f"La reserva {self.id_reserva} ya está cancelada.")

            self.estado = "Cancelada"
            msg = "Reserva cancelada correctamente."
            print(f"[AVISO] {msg}")
            self.registrar_log(msg)
        except ReservaError as e:
            error_msg = f"Error al cancelar: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg, es_error=True)
            raise

    def calcular_costo_reserva(self, *args, **kwargs):
        """
        Calcula el costo total invocando polimórficamente al método del servicio
        (aprovecha la sobrecarga y parámetros opcionales de cada tipo de servicio).
        """
        try:
            costo_total = self.servicio.calcular_costo(self.cantidad, *args, **kwargs)
        except Exception as e:
            error_msg = f"Error calculando el costo de la reserva: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg, es_error=True)
            # AJUSTE: encadenamiento, la causa original queda en __cause__
            raise ReservaNoValidaError(error_msg) from e
        else:  # AJUSTE: solo se ejecuta si el cálculo NO falló
            self.registrar_log(f"Costo calculado exitosamente: ${costo_total}")
            return costo_total

    def obtener_descripcion(self):
        return (
            f"ID Reserva: {self.id_reserva} | Estado: {self.estado} | "
            f"Cantidad: {self.cantidad:g} | Cliente: [{self.cliente.nombre}] | "
            f"Servicio: {self.servicio.obtener_descripcion()}"
        )
