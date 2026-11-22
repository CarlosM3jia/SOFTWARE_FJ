# Archivo: main.py
# Punto de entrada: integra los módulos de Clientes, Servicios y Reservas y
# simula 15 operaciones completas (válidas e inválidas) de Software FJ,
# sin usar bases de datos.
# Ejecutar con:  python main.py

from modelos.cliente import Cliente  # Módulo de Clientes: clase Cliente
from modelos.gestor_clientes import GestorClientes  # Módulo de Clientes: gestor
from servicios.servicios import (  # Módulo de Servicios: servicios especializados
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)
from reservas.reserva import Reserva, ReservaError  # Módulo de Reservas
from excepciones.excepciones_clientes import ErrorCliente  # Errores de clientes
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
    except (ErrorCliente, ReservaError, ValueError) as error:  # Errores controlados
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


def op_servicio_tarifa_no_numerica():
    # La tarifa no es numérica: Python lanza ValueError al convertirla
    return AlquilerEquipos("EQ-999", "gratis", "Monitor")


def op_servicio_tarifa_cero():
    # La tarifa debe ser mayor a cero: el servicio rechaza el dato
    return AsesoriaEspecializada("ASES-000", 0, "Desarrollo Cloud")


def op_servicios_equipo_y_asesoria():
    equipo = AlquilerEquipos("EQ-202", 80000, "Servidor Rack")  # Equipo
    asesoria = AsesoriaEspecializada("ASES-303", 120000, "Desarrollo Cloud")
    servicios_registrados.extend([equipo, asesoria])  # Se guardan ambos
    # Polimorfismo: el mismo método calcular_costo, resultados distintos
    costo_equipo = equipo.calcular_costo(3, seguro=20000)
    costo_asesoria = asesoria.calcular_costo(2, bono_especial=30000)
    return f"Equipo 3 días = ${costo_equipo} | Asesoría 2 sesiones = ${costo_asesoria}"


def op_reserva_exitosa():
    # INTEGRACIÓN: Cliente (gestor) + Servicio (lista) + Reserva
    cliente = gestor.buscar_cliente("1070123456")  # Cliente registrado
    reserva = Reserva("RES-001", cliente, servicios_registrados[0], 4)  # Sala 4 h
    reservas.append(reserva)  # Se guarda en la lista de reservas
    reserva.confirmar_reserva()  # Pendiente -> Confirmada
    costo = reserva.calcular_costo_reserva(descuento_porcentaje=10)  # Polimorfismo
    return f"{reserva.obtener_descripcion()} | Total: ${costo}"


def op_reserva_cantidad_invalida():
    cliente = gestor.buscar_cliente("1070654321")  # Segundo cliente
    # Cantidad negativa: debe lanzar ReservaNoValidaError
    return Reserva("RES-002", cliente, servicios_registrados[2], -3)


def op_reserva_confirmar_dos_veces():
    # RES-001 ya está confirmada: debe lanzar ReservaError
    return reservas[0].confirmar_reserva()


def op_reserva_cancelar_y_reconfirmar():
    cliente = gestor.buscar_cliente("1070654321")
    reserva = Reserva("RES-003", cliente, servicios_registrados[2], 2)  # Asesoría
    reservas.append(reserva)  # Se guarda en la lista
    reserva.cancelar_reserva()  # Pendiente -> Cancelada
    return reserva.confirmar_reserva()  # Falla: ReservaError


def op_calculo_inconsistente():
    cliente = gestor.buscar_cliente("1070123456")
    reserva = Reserva("RES-004", cliente, servicios_registrados[0], 2)  # Sala 2 h
    reservas.append(reserva)  # Se guarda en la lista
    # Un descuento de 150 % es inconsistente: el ValueError del servicio queda
    # encadenado dentro de un ReservaNoValidaError (raise ... from ...)
    return reserva.calcular_costo_reserva(descuento_porcentaje=150)


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
        ("Servicio con tarifa no numérica", op_servicio_tarifa_no_numerica),
        ("Servicio con tarifa en cero", op_servicio_tarifa_cero),
        ("Crear equipo y asesoría (polimorfismo)", op_servicios_equipo_y_asesoria),
        ("Reserva exitosa (confirmar y calcular costo)", op_reserva_exitosa),
        ("Reserva con cantidad negativa", op_reserva_cantidad_invalida),
        ("Confirmar dos veces la misma reserva", op_reserva_confirmar_dos_veces),
        ("Cancelar y volver a confirmar una reserva", op_reserva_cancelar_y_reconfirmar),
        ("Cálculo inconsistente (descuento 150%)", op_calculo_inconsistente),
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
