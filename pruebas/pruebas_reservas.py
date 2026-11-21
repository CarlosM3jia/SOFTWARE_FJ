from modelos.cliente import Cliente
from servicios.servicios import ReservaSala
from reservas.reserva import Reserva, ReservaNoValidaError

print("--- INICIANDO PRUEBAS DEL MÓDULO DE RESERVAS ---")

try:
    #1creamos un cliente válido
    cliente1 = Cliente("10203040", "Carlos Perez", "carlos@mail.com", "3101234567")
    
    #2.creamos un servicio válido (Reserva de Sala)
    sala = ReservaSala("SALA-01", 50000, 10)
    
    #3creamos una reserva válida
    reserva1 = Reserva("RES-001", cliente1, sala, 3)
    print(reserva1.obtener_descripcion())
    
    #Probar cálculo de costos con polimorfismo
    costo = reserva1.calcular_costo_reserva(descuento_porcentaje=10, impuesto=0.19)
    print(f"Costo total calculado: ${costo}")
    
    #confirmación
    reserva1.confirmar_reserva()

    #4.prueba de error (Cantidad inválida para activar excepciones)
    print("\n--- Probando manejo de excepciones ---")
    reserva_errada = Reserva("RES-002", cliente1, sala, -2)

except (ReservaNoValidaError, ValueError) as e:
    print(f"[CAPTURA DE EXCEPCIÓN EXITOSA] El sistema atrapó el error: {e}")

print("--- PRUEBAS FINALIZADAS CORRECTAMENTE ---")