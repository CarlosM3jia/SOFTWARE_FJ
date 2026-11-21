import os
from datetime import datetime

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
        
        if cantidad <= 0:
            raise ReservaNoValidaError("La cantidad (horas/días/sesiones) debe ser mayor a cero.")
        
        self.cantidad = cantidad
        self.estado = "Pendiente"  # Estados posibles: Pendiente, Confirmada, Cancelada
        self.fecha_creacion = datetime.now()

    def registrar_log(self, mensaje):
        """Registra eventos y errores en un archivo de logs de la empresa sin usar BD."""
        os.makedirs("excepciones", exist_ok=True)
        ruta_log = os.path.join("excepciones", "log_sistema.txt")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ruta_log, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{timestamp}] - RESERVA {self.id_reserva}: {mensaje}\n")

    def confirmar_reserva(self):
        try:
            if self.estado == "Confirmada":
                raise ReservaError(f"La reserva {self.id_reserva} ya se encontraba confirmada previamente.")
            if self.estado == "Cancelada":
                raise ReservaError(f"No se puede confirmar una reserva que ya fue cancelada.")
            
            self.estado = "Confirmada"
            msg = f"Reserva confirmada con éxito para el cliente {self.cliente.nombre}."
            print(f"[EXITO] {msg}")
            self.registrar_log(msg)
        except ReservaError as e:
            error_msg = f"Error al intentar confirmar: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg)
            raise
        finally:
            print(f"-> Proceso de confirmación finalizado para la reserva {self.id_reserva}.\n")

    def cancelar_reserva(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaError(f"La reserva {self.id_reserva} ya está cancelada.")
            
            self.estado = "Cancelada"
            msg = f"Reserva cancelada correctamente."
            print(f"[AVISO] {msg}")
            self.registrar_log(msg)
        except ReservaError as e:
            error_msg = f"Error al cancelar: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg)
            raise

    def calcular_costo_reserva(self, *args, **kwargs):
        """
        Calcula el costo total invocando polimórficamente al método del servicio 
        (aprovecha la sobrecarga y parámetros opcionales de cada tipo de servicio).
        """
        try:
            costo_total = self.servicio.calcular_costo(self.cantidad, *args, **kwargs)
            self.registrar_log(f"Costo calculado exitosamente: ${costo_total}")
            return costo_total
        except Exception as e:
            error_msg = f"Error calculando el costo de la reserva: {e}"
            print(f"[LOG ERROR] {error_msg}")
            self.registrar_log(error_msg)
            raise ReservaNoValidaError(error_msg)

    def obtener_descripcion(self):
        return (
            f"ID Reserva: {self.id_reserva} | Estado: {self.estado} | "
            f"Cantidad: {self.cantidad} | Cliente: [{self.cliente.nombre}] | "
            f"Servicio: {self.servicio.obtener_descripcion()}"
        )