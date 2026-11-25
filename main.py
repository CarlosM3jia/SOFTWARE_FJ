
from modelos.cliente import Cliente
from modelos.gestor_clientes import GestorClientes

from servicios.servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)

from reservas.reserva import Reserva


def ejecutar_operacion(numero, descripcion, accion):
    """Ejecuta una operación y controla sus posibles excepciones."""
    print(f"\n--- OPERACION {numero}: {descripcion} ---")

    try:
        resultado = accion()

        if resultado is not None:
            print(resultado)

        print("[CORRECTO] Operacion finalizada.")

    except Exception as error:
        print(f"[ERROR CONTROLADO] {type(error).__name__}: {error}")
        print("[SISTEMA] El programa continua ejecutandose.")


def main():
    print("=" * 55)
    print("       SISTEMA DE GESTION SOFTWARE FJ")
    print("=" * 55)

    # Crear el gestor de clientes.
    gestor = GestorClientes()

    # Crear clientes.
    cliente1 = Cliente(
        "10203040",
        "Carlos Perez",
        "carlos@mail.com",
        "3101234567"
    )

    cliente2 = Cliente(
        "50607080",
        "Maria Gomez",
        "maria@mail.com",
        "3201234567"
    )

    # Crear los servicios.
    sala = ReservaSala("SALA-01", 50000, 10)

    equipo = AlquilerEquipos(
        "EQ-01",
        80000,
        "Computador"
    )

    asesoria = AsesoriaEspecializada(
        "ASE-01",
        100000,
        "Desarrollo de software"
    )

    # Crear una reserva.
    reserva1 = Reserva("RES-001", cliente1, sala, 3)

    # Operaciones de clientes.
    ejecutar_operacion(
        1, "Registrar primer cliente",
        lambda: gestor.registrar_cliente(cliente1)
    )

    ejecutar_operacion(
        2, "Registrar segundo cliente",
        lambda: gestor.registrar_cliente(cliente2)
    )

    ejecutar_operacion(
        3, "Buscar cliente",
        lambda: gestor.buscar_cliente("10203040").obtener_descripcion()
    )

    ejecutar_operacion(
        4, "Actualizar datos del cliente",
        lambda: gestor.actualizar_cliente(
            "10203040",
            telefono="3117654321"
        )
    )

    ejecutar_operacion(
        5, "Consultar cantidad de clientes",
        lambda: f"Clientes registrados: {gestor.cantidad_clientes()}"
    )

    ejecutar_operacion(
        6, "Listar clientes",
        lambda: "\n".join(
            cliente.obtener_descripcion()
            for cliente in gestor.listar_clientes()
        )
    )

    # Operaciones de servicios.
    ejecutar_operacion(
        7, "Consultar reserva de sala",
        lambda: sala.obtener_descripcion()
    )

    ejecutar_operacion(
        8, "Calcular costo de sala",
        lambda: f"Costo total: ${sala.calcular_costo(3, 10, 0.19)}"
    )

    ejecutar_operacion(
        9, "Consultar alquiler de equipos",
        lambda: equipo.obtener_descripcion()
    )

    ejecutar_operacion(
        10, "Calcular alquiler de equipos",
        lambda: f"Costo total: ${equipo.calcular_costo(2, 15000)}"
    )

    ejecutar_operacion(
        11, "Calcular asesoria especializada",
        lambda: f"Costo total: ${asesoria.calcular_costo(3, 20000)}"
    )

    # Operaciones de reservas.
    ejecutar_operacion(
        12, "Consultar reserva",
        lambda: reserva1.obtener_descripcion()
    )

    ejecutar_operacion(
        13, "Calcular costo de la reserva",
        lambda: f"Costo total: ${reserva1.calcular_costo_reserva(
            descuento_porcentaje=10,
            impuesto=0.19
        )}"
    )

    ejecutar_operacion(
        14, "Confirmar reserva",
        lambda: reserva1.confirmar_reserva()
    )

    ejecutar_operacion(
        15, "Cancelar reserva",
        lambda: reserva1.cancelar_reserva()
    )

    # Operaciones con datos inválidos.
    ejecutar_operacion(
        16, "Intentar registrar cliente duplicado",
        lambda: gestor.registrar_cliente(cliente1)
    )

    ejecutar_operacion(
        17, "Buscar cliente inexistente",
        lambda: gestor.buscar_cliente("99999999")
    )

    ejecutar_operacion(
        18, "Intentar crear reserva con cantidad negativa",
        lambda: Reserva("RES-002", cliente1, sala, -2)
    )

    ejecutar_operacion(
        19, "Intentar calcular sala con cero horas",
        lambda: sala.calcular_costo(0)
    )

    print("\n" + "=" * 55)
    print("       FIN DE LAS OPERACIONES DE SOFTWARE FJ")
    print("=" * 55)


if __name__ == "__main__":
    main()
