# Archivo: main.py
# Punto de entrada: simula 14 operaciones completas (válidas e inválidas)
# del sistema Software FJ sin usar bases de datos.
# Ejecutar con:  python main.py

from modelos.cliente import Cliente  # Clase Cliente
from modelos.gestor_clientes import GestorClientes  # Administra los clientes
from modelos.reserva import Reserva  # Clase Reserva
from servicios.servicios import (  # Servicios especializados
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from excepciones.excepciones_clientes import ErrorCliente  # Errores de clientes
from excepciones.excepciones_servicios import ErrorServicio, ErrorReserva  # Idem
from utilidades.logger import (  # Funciones para escribir en el log
    registrar_evento,
    registrar_error,
    registrar_critico,
    ARCHIVO_LOG
)

# ---------- Listas internas (reemplazan a la base de datos) ----------
gestor = GestorClientes()  # Guarda los clientes en memoria
servicios_registrados = []  # Lista de servicios creados correctamente
reservas = []  # Lista de reservas creadas correctamente

# Contadores para el resumen final
estadisticas = {"exitosas": 0, "controladas": 0, "inesperadas": 0}


def ejecutar_operacion(numero, titulo, funcion):
    """
    Ejecuta una operación protegida: si falla, registra el error y
    el programa CONTINÚA con la siguiente operación.
    """
    print(f"\n--- Operación {numero}: {titulo}")  # Encabezado en consola
    registrar_evento(f"Inicio de la operación {numero}: {titulo}")  # Log
    try:  # Bloque que puede fallar
        resultado = funcion()  # Ejecuta la operación recibida
    except (ErrorCliente, ErrorServicio, ErrorReserva) as error:  # Controlados
        estadisticas["controladas"] += 1  # Suma al contador de errores controlados
        registrar_error(f"Operación {numero} falló (error controlado)", error)
        print(f"   [ERROR CONTROLADO] {error}")  # Muestra el error
        if error.__cause__ is not None:  # Si el error fue encadenado...
            print(f"   (causa original: {error.__cause__})")  # ...muestra la causa
    except Exception as error:  # Cualquier otro error inesperado
        estadisticas["inesperadas"] += 1  # Suma al contador de inesperados
        registrar_critico(f"Operación {numero} falló (error inesperado)", error)
        print(f"   [ERROR INESPERADO] {type(error).__name__}: {error}")
    else:  # Solo se ejecuta si NO hubo excepción
        estadisticas["exitosas"] += 1  # Suma al contador de éxitos
        registrar_evento(f"Operación {numero} exitosa: {resultado}")  # Log
        print(f"   [OK] {resultado}")  # Muestra el resultado
    finally:  # Se ejecuta SIEMPRE
        registrar_evento(f"Fin de la operación {numero}")  # Cierra el registro


# ---------- Operaciones de la simulación ----------

def op_cliente_valido_1():
    cliente = Cliente("1070123456", "laura gomez", "laura@correo.com", "3001234567")
    return gestor.registrar_cliente(cliente) + f" ({cliente.nombre})"


def op_cliente_valido_2():
    cliente = Cliente("1070654321", "Andres Rojas", "andres@correo.com", "3109876543")
    return gestor.registrar_cliente(cliente) + f" ({cliente.nombre})"


def op_cliente_correo_invalido():
    # El correo no tiene formato válido: debe lanzar DatosClienteInvalidos
    return gestor.registrar_cliente(
        Cliente("1070111222", "Pedro Diaz", "correo-sin-arroba", "3201112233")
    )


def op_cliente_telefono_invalido():
    # El teléfono tiene letras: debe lanzar DatosClienteInvalidos
    return gestor.registrar_cliente(
        Cliente("1070333444", "Marta Ruiz", "marta@correo.com", "abc123")
    )


def op_cliente_duplicado():
    # Misma identificación que la operación 1: debe lanzar ErrorCliente
    return gestor.registrar_cliente(
        Cliente("1070123456", "Laura Duplicada", "otra@correo.com", "3005556677")
    )


def op_servicio_sala_valido():
    sala = ReservaSala("SALA-101", 50000, 20)  # Sala de 20 personas
    servicios_registrados.append(sala)  # Se guarda en la lista interna
    costo = sala.calcular_costo(4, descuento_porcentaje=10)  # Con descuento
    return f"{sala.obtener_descripcion()} | 4 h con 10% dto + IVA = ${costo}"


def op_servicio_tarifa_invalida():
    # La tarifa no es numérica: el ValueError de Python queda encadenado
    return AlquilerEquipos("EQ-999", "gratis", "Monitor")


def op_servicios_equipo_y_asesoria():
    equipo = AlquilerEquipos("EQ-202", 80000, "Servidor Rack")  # Equipo
    asesoria = AsesoriaEspecializada("ASES-303", 120000, "Desarrollo Cloud")
    servicios_registrados.extend([equipo, asesoria])  # Se guardan ambos
    # Polimorfismo: el mismo método calcular_costo, resultados distintos
    costo_equipo = equipo.calcular_costo(3, seguro=20000)
    costo_asesoria = asesoria.calcular_costo(2, bono_especial=30000)
    return f"Equipo 3 días = ${costo_equipo} | Asesoría 2 sesiones = ${costo_asesoria}"


def op_reserva_exitosa():
    cliente = gestor.buscar_cliente("1070123456")  # Cliente registrado
    reserva = Reserva("RES-001", cliente, servicios_registrados[0], 4)  # Sala 4 h
    reservas.append(reserva)  # Se guarda en la lista de reservas
    reserva.confirmar()  # PENDIENTE -> CONFIRMADA
    reserva.procesar(descuento_porcentaje=10)  # CONFIRMADA -> PROCESADA
    return reserva.obtener_descripcion()


def op_reserva_servicio_no_disponible():
    cliente = gestor.buscar_cliente("1070654321")  # Segundo cliente
    equipo = servicios_registrados[1]  # El equipo creado antes
    equipo.establecer_disponibilidad(False)  # Se desactiva el servicio
    reserva = Reserva("RES-002", cliente, equipo, 2)  # Se crea la reserva
    reservas.append(reserva)  # Queda pendiente en la lista
    return reserva.confirmar()  # Falla: ServicioNoDisponible


def op_reserva_duracion_invalida():
    cliente = gestor.buscar_cliente("1070654321")
    # Duración negativa: debe lanzar ReservaInvalida
    return Reserva("RES-003", cliente, servicios_registrados[2], -3)


def op_reserva_cancelar_y_reconfirmar():
    cliente = gestor.buscar_cliente("1070654321")
    reserva = Reserva("RES-004", cliente, servicios_registrados[2], 2)  # Asesoría
    reservas.append(reserva)  # Se guarda en la lista
    reserva.cancelar()  # PENDIENTE -> CANCELADA
    return reserva.confirmar()  # Falla: OperacionNoPermitida


def op_calculo_inconsistente():
    cliente = gestor.buscar_cliente("1070123456")  # Cliente registrado
    reserva = Reserva("RES-005", cliente, servicios_registrados[2], 2)  # Asesoría
    reservas.append(reserva)  # Se guarda en la lista de reservas
    reserva.confirmar()  # PENDIENTE -> CONFIRMADA
    # Un bono mayor al costo total es inconsistente: el error de cálculo
    # queda encadenado dentro de un ErrorReserva (raise ... from ...)
    return reserva.procesar(bono_especial=999999999)


def op_error_inesperado():
    # Se pide una reserva que no existe: IndexError (error NO previsto)
    return reservas[99].obtener_descripcion()


# ---------- Programa principal ----------

def main():
    registrar_evento("===== INICIO DE LA SIMULACIÓN SOFTWARE FJ =====")  # Log
    print("=== SOFTWARE FJ: SIMULACIÓN DE OPERACIONES ===")  # Título

    operaciones = [  # Lista de (título, función) en orden de ejecución
        ("Registrar cliente válido", op_cliente_valido_1),
        ("Registrar segundo cliente válido", op_cliente_valido_2),
        ("Cliente con correo inválido", op_cliente_correo_invalido),
        ("Cliente con teléfono inválido", op_cliente_telefono_invalido),
        ("Cliente con identificación duplicada", op_cliente_duplicado),
        ("Crear servicio de sala y calcular costo", op_servicio_sala_valido),
        ("Servicio con tarifa no numérica", op_servicio_tarifa_invalida),
        ("Crear equipo y asesoría (polimorfismo)", op_servicios_equipo_y_asesoria),
        ("Reserva exitosa (confirmar y procesar)", op_reserva_exitosa),
        ("Reserva con servicio no disponible", op_reserva_servicio_no_disponible),
        ("Reserva con duración negativa", op_reserva_duracion_invalida),
        ("Cancelar y volver a confirmar una reserva", op_reserva_cancelar_y_reconfirmar),
        ("Cálculo inconsistente (bono mayor al costo)", op_calculo_inconsistente),
        ("Error inesperado (reserva inexistente)", op_error_inesperado),
    ]

    for numero, (titulo, funcion) in enumerate(operaciones, start=1):  # Una a una
        ejecutar_operacion(numero, titulo, funcion)  # El programa no se detiene

    # ----- Resumen final -----
    print("\n=== RESUMEN ===")
    print(f"Operaciones ejecutadas: {len(operaciones)}")
    print(f"Exitosas: {estadisticas['exitosas']}")
    print(f"Errores controlados: {estadisticas['controladas']}")
    print(f"Errores inesperados (también registrados): {estadisticas['inesperadas']}")
    print(f"Clientes registrados: {gestor.cantidad_clientes()}")
    print(f"Servicios creados: {len(servicios_registrados)}")
    print("Reservas:")
    for reserva in reservas:  # Recorre la lista interna de reservas
        print(f"  - {reserva.obtener_descripcion()}")
    print(f"\nRegistro completo de eventos y errores en: {ARCHIVO_LOG}")
    registrar_evento("===== FIN DE LA SIMULACIÓN SOFTWARE FJ =====")  # Log


if __name__ == "__main__":  # Solo se ejecuta al correr este archivo directamente
    main()
