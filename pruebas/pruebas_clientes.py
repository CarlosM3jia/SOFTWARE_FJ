
from modelos.cliente import Cliente
from modelos.gestor_clientes import GestorClientes
from excepciones.excepciones_clientes import (
    DatosClienteInvalidos,
    ClienteNoEncontrado,
    ErrorCliente
)


def probar_gestor_clientes():
    gestor = GestorClientes()

    print("\n===== PRUEBA 1: REGISTRO DE CLIENTES =====")

    cliente1 = Cliente(
        "123456789",
        "Carlos Mejia",
        "carlos@gmail.com",
        "3001234567"
    )

    cliente2 = Cliente(
        "987654321",
        "Juan Perez",
        "juan@gmail.com",
        "3101234567"
    )

    print(gestor.registrar_cliente(cliente1))
    print(gestor.registrar_cliente(cliente2))

    print("\n===== PRUEBA 2: BUSQUEDA =====")

    encontrado = gestor.buscar_cliente("123456789")
    print(encontrado.obtener_descripcion())

    print("\n===== PRUEBA 3: ACTUALIZACION =====")

    print(
        gestor.actualizar_cliente(
            "123456789",
            correo="carlos2026@gmail.com"
        )
    )

    print(gestor.buscar_cliente("123456789").obtener_descripcion())

    print("\n===== PRUEBA 4: LISTADO =====")

    for cliente in gestor.listar_clientes():
        print(cliente.obtener_descripcion())

    print("\nCantidad de clientes:", gestor.cantidad_clientes())

    print("\n===== PRUEBA 5: IDENTIFICACION DUPLICADA =====")

    try:
        gestor.registrar_cliente(cliente1)
    except ErrorCliente as error:
        print("Error controlado:", error)

    print("\n===== PRUEBA 6: CLIENTE INEXISTENTE =====")

    try:
        gestor.buscar_cliente("111111111")
    except ClienteNoEncontrado as error:
        print("Error controlado:", error)

    print("\n===== PRUEBA 7: DATOS INVALIDOS =====")

    try:
        Cliente(
            "555555555",
            "Ana",
            "correo_invalido",
            "3001234567"
        )
    except DatosClienteInvalidos as error:
        print("Error controlado:", error)

    print("\n===== PRUEBA 8: ELIMINACION =====")

    print(gestor.eliminar_cliente("987654321"))

    print("Clientes restantes:", gestor.cantidad_clientes())

    print("\n===== TODAS LAS PRUEBAS FINALIZARON =====")


if __name__ == "__main__":
    probar_gestor_clientes()
