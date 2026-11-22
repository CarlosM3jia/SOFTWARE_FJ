
from servicios.servicios import (
    ReservaSala,
    AlquilerEquipos,
    AsesoriaEspecializada
)

print("\n===== PRUEBAS DEL MODULO DE SERVICIOS =====")

# 1. Prueba de reserva de sala
print("\n--- 1. RESERVA DE SALA ---")

sala = ReservaSala("SALA-01", 50000, 10)

print(sala.obtener_descripcion())

costo_sala = sala.calcular_costo(
    3,
    descuento_porcentaje=10,
    impuesto=0.19
)

print(f"Costo de la reserva de sala: ${costo_sala}")


# 2. Prueba de alquiler de equipos
print("\n--- 2. ALQUILER DE EQUIPOS ---")

equipo = AlquilerEquipos("EQ-01", 80000, "Computador")

print(equipo.obtener_descripcion())

costo_equipo = equipo.calcular_costo(
    2,
    seguro=15000
)

print(f"Costo del alquiler de equipo: ${costo_equipo}")


# 3. Prueba de asesoria especializada
print("\n--- 3. ASESORIA ESPECIALIZADA ---")

asesoria = AsesoriaEspecializada(
    "ASE-01",
    100000,
    "Desarrollo de software"
)

print(asesoria.obtener_descripcion())

costo_asesoria = asesoria.calcular_costo(
    3,
    bono_especial=20000
)

print(f"Costo de la asesoria: ${costo_asesoria}")


# 4. Pruebas de manejo de excepciones
print("\n--- 4. MANEJO DE EXCEPCIONES ---")

try:
    sala.calcular_costo(0)
except ValueError as error:
    print(f"Excepcion de sala controlada: {error}")

try:
    equipo.calcular_costo(-2)
except ValueError as error:
    print(f"Excepcion de equipo controlada: {error}")

try:
    asesoria.calcular_costo(0)
except ValueError as error:
    print(f"Excepcion de asesoria controlada: {error}")


print("\n===== TODAS LAS PRUEBAS FINALIZARON =====")
