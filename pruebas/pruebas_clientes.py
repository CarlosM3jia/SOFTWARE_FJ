
from modelos.cliente import Cliente
from excepciones.excepciones_clientes import DatosClienteInvalidos


def probar_registro_cliente():
    print("\n===== PRUEBA 1: REGISTRO DE CLIENTE =====")

    cliente = Cliente(
        "123456789",
        "carlos mejia",
        "carlos@gmail.com",
        "3001234567"
    )

    print("Cliente registrado correctamente.")
    print(cliente.obtener_descripcion())


def probar_correo_invalido():
    print("\n===== PRUEBA 2: CORREO INVALIDO =====")

    try:
        cliente = Cliente(
            "987654321",
            "Juan Perez",
            "correo_incorrecto",
            "3101234567"
        )

    except DatosClienteInvalidos as error:
        print("Error controlado correctamente:")
        print(error)


def probar_actualizacion():
    print("\n===== PRUEBA 3: ACTUALIZACION =====")

    cliente = Cliente(
        "456789123",
        "Maria Lopez",
        "maria@gmail.com",
        "3151234567"
    )

    cliente.actualizar_datos(correo="maria2026@gmail.com")

    print(cliente.obtener_descripcion())


if __name__ == "__main__":
    probar_registro_cliente()
    probar_correo_invalido()
    probar_actualizacion()

    print("\n===== TODAS LAS PRUEBAS FINALIZARON =====")
