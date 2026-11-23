
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
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from servicios.servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada

def ejecutar_pruebas_servicios():
    print("=== INICIANDO PRUEBAS DEL MÓDULO DE SERVICIOS ===\n")

    # 1. Prueba válida: Reserva de Sala (con y sin sobrecarga)
    try:
        sala = ReservaSala("SALA-101", 50000, 20)
        print("1. Creación exitosa:", sala.obtener_descripcion())
        print(f"   -> Costo base (4h + IVA): ${sala.calcular_costo(4)}")
        print(f"   -> Costo con sobrecarga (4h, 10% dto + IVA): ${sala.calcular_costo(4, descuento_porcentaje=10)}\n")
    except ValueError as e:
        print(f"   -> Error inesperado: {e}\n")

    # 2. Prueba válida: Alquiler de Equipos (con seguro opcional)
    try:
        equipo = AlquilerEquipos("EQ-202", 80000, "Servidor Rack")
        print("2. Creación exitosa:", equipo.obtener_descripcion())
        print(f"   -> Costo por 3 días con seguro: ${equipo.calcular_costo(3, seguro=20000)}\n")
    except ValueError as e:
        print(f"   -> Error inesperado: {e}\n")

    # 3. Prueba válida: Asesoría Especializada (con bono de descuento)
    try:
        asesoria = AsesoriaEspecializada("ASES-303", 120000, "Desarrollo Cloud")
        print("3. Creación exitosa:", asesoria.obtener_descripcion())
        print(f"   -> Costo por 2 sesiones con bono: ${asesoria.calcular_costo(2, bono_especial=30000)}\n")
    except ValueError as e:
        print(f"   -> Error inesperado: {e}\n")

    # 4. Prueba inválida (Excepción controlada por horas negativas)
    try:
        print("4. Probando validación de error (horas negativas en sala)...")
        sala.calcular_costo(-5)
    except ValueError as e:
        print(f"   -> Excepción capturada correctamente: {e}\n")

    # 5. Prueba inválida (Excepción controlada por tarifa en cero)
    try:
        print("5. Probando validación de error (tarifa base en cero)...")
        servicio_malo = AlquilerEquipos("EQ-999", 0, "Monitor")
    except ValueError as e:
        print(f"   -> Excepción capturada correctamente: {e}\n")

    print("=== PRUEBAS FINALIZADAS CON ÉXITO ===")

if __name__ == "__main__":
    ejecutar_pruebas_servicios()
