# Archivo: pruebas/pruebas_generales.py
# Pruebas generales del sistema completo: integración de Clientes, Servicios,
# Reservas, manejo de excepciones y registro en el archivo de logs.
# Ejecutar con:  python pruebas/pruebas_generales.py

import os  # Rutas y variables de entorno
import sys  # Ruta de búsqueda de módulos y del intérprete
import subprocess  # Para ejecutar main.py como lo haría un usuario
import tempfile  # Carpeta temporal para no ensuciar el log real
import unittest  # Marco de pruebas incluido en Python

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Raíz
sys.path.insert(0, RAIZ)  # Permite importar los módulos del proyecto

CARPETA_LOGS_PRUEBA = tempfile.mkdtemp()  # Carpeta temporal para los logs
os.environ["SOFTWARE_FJ_LOG_DIR"] = CARPETA_LOGS_PRUEBA  # Antes de importar

from modelos.entidad import Entidad  # noqa: E402
from modelos.cliente import Cliente  # noqa: E402
from modelos.gestor_clientes import GestorClientes  # noqa: E402
from servicios.servicios import (  # noqa: E402
    Servicio, ReservaSala, AlquilerEquipos, AsesoriaEspecializada
)
from reservas.reserva import Reserva, ReservaError, ReservaNoValidaError  # noqa: E402
from excepciones.excepciones_clientes import (  # noqa: E402
    DatosClienteInvalidos, ErrorCliente, ClienteNoEncontrado
)


def crear_cliente():
    """Devuelve un cliente válido para usar en las pruebas."""
    return Cliente("1070123456", "Laura Gomez", "laura@correo.com", "3001234567")


class PruebasAbstraccion(unittest.TestCase):
    def test_clases_abstractas_no_se_instancian(self):
        with self.assertRaises(TypeError):  # Entidad es abstracta
            Entidad("1")
        with self.assertRaises(TypeError):  # Servicio es abstracta
            Servicio("S1", "Generico", 100)

    def test_herencia(self):
        self.assertTrue(issubclass(Cliente, Entidad))  # Cliente es Entidad
        for clase in (ReservaSala, AlquilerEquipos, AsesoriaEspecializada):
            self.assertTrue(issubclass(clase, Servicio))  # Los 3 son Servicio


class PruebasClientes(unittest.TestCase):
    def test_cliente_valido_normaliza_datos(self):
        cliente = Cliente("1070123456", "  laura gomez ", "LAURA@Correo.com", "3001234567")
        self.assertEqual(cliente.nombre, "Laura Gomez")  # Capitaliza
        self.assertEqual(cliente.correo, "laura@correo.com")  # Minúsculas

    def test_datos_invalidos(self):
        casos = [
            ("1070123456", "Al", "l@c.com", "3001234567"),  # Nombre corto
            ("1070123456", "Laura", "sin-arroba", "3001234567"),  # Correo
            ("1070123456", "Laura", "l@c.com", "12ab"),  # Teléfono
        ]
        for caso in casos:
            with self.assertRaises(DatosClienteInvalidos):
                Cliente(*caso)

    def test_gestor_duplicado_y_no_encontrado(self):
        gestor = GestorClientes()
        gestor.registrar_cliente(crear_cliente())
        with self.assertRaises(ErrorCliente):  # Duplicado
            gestor.registrar_cliente(crear_cliente())
        with self.assertRaises(ClienteNoEncontrado):  # Inexistente
            gestor.buscar_cliente("999999999")


class PruebasServicios(unittest.TestCase):
    def test_polimorfismo_de_costos(self):
        self.assertEqual(ReservaSala("S1", 50000, 20).calcular_costo(4), 238000.0)
        self.assertEqual(AlquilerEquipos("E1", 80000, "Rack").calcular_costo(3, seguro=20000), 260000.0)
        self.assertEqual(AsesoriaEspecializada("A1", 120000, "Cloud").calcular_costo(2, bono_especial=30000), 210000.0)

    def test_sobrecarga_con_parametros_opcionales(self):
        sala = ReservaSala("S1", 50000, 20)
        self.assertEqual(sala.calcular_costo(4, descuento_porcentaje=10), 214200.0)
        self.assertEqual(sala.calcular_costo(4, impuesto=0), 200000.0)

    def test_errores_de_servicio(self):
        sala = ReservaSala("S1", 50000, 20)
        with self.assertRaises(ValueError):  # Horas negativas
            sala.calcular_costo(-1)
        with self.assertRaises(ValueError):  # Descuento fuera de rango
            sala.calcular_costo(2, descuento_porcentaje=150)
        with self.assertRaises(ValueError):  # Tarifa en cero
            AlquilerEquipos("E1", 0, "Monitor")
        with self.assertRaises(ValueError):  # Código vacío
            ReservaSala("", 100, 5)


class PruebasReservas(unittest.TestCase):
    def setUp(self):
        self.reserva = Reserva("R1", crear_cliente(), ReservaSala("S1", 50000, 20), 4)

    def test_flujo_completo(self):
        self.assertEqual(self.reserva.estado, "Pendiente")
        self.reserva.confirmar_reserva()
        self.assertEqual(self.reserva.estado, "Confirmada")
        self.assertEqual(self.reserva.calcular_costo_reserva(descuento_porcentaje=10), 214200.0)

    def test_operaciones_no_permitidas(self):
        self.reserva.confirmar_reserva()
        with self.assertRaises(ReservaError):  # Confirmar dos veces
            self.reserva.confirmar_reserva()
        self.reserva.cancelar_reserva()
        with self.assertRaises(ReservaError):  # Confirmar una cancelada
            self.reserva.confirmar_reserva()
        with self.assertRaises(ReservaError):  # Cancelar dos veces
            self.reserva.cancelar_reserva()

    def test_reserva_invalida(self):
        servicio = ReservaSala("S1", 50000, 20)
        with self.assertRaises(ReservaNoValidaError):
            Reserva("R3", crear_cliente(), servicio, -3)  # Cantidad negativa
        with self.assertRaises(ReservaNoValidaError):
            Reserva("R3", crear_cliente(), servicio, "mucho")  # No numérica

    def test_encadenamiento_en_calculo(self):
        with self.assertRaises(ReservaNoValidaError) as contexto:
            self.reserva.calcular_costo_reserva(descuento_porcentaje=150)
        self.assertIsInstance(contexto.exception.__cause__, ValueError)  # Causa


class PruebaSistemaCompleto(unittest.TestCase):
    def test_main_no_se_detiene_y_registra_el_log(self):
        carpeta = tempfile.mkdtemp()  # Log exclusivo de esta prueba
        entorno = dict(os.environ, SOFTWARE_FJ_LOG_DIR=carpeta)  # Entorno propio
        resultado = subprocess.run(  # Ejecuta main.py como un usuario real
            [sys.executable, os.path.join(RAIZ, "main.py")],
            capture_output=True, text=True, encoding="utf-8", env=entorno
        )
        self.assertEqual(resultado.returncode, 0)  # Terminó sin caerse
        self.assertIn("Operaciones ejecutadas: 15", resultado.stdout)  # >= 10
        with open(os.path.join(carpeta, "software_fj.log"), encoding="utf-8") as f:
            lineas = f.read().splitlines()  # Lee el log generado
        errores = [l for l in lineas if "| ERROR |" in l]
        criticos = [l for l in lineas if "| CRITICAL |" in l]
        self.assertGreaterEqual(len(errores), 9)  # Errores controlados registrados
        self.assertEqual(len(criticos), 1)  # El error inesperado también
        self.assertTrue(any("causa:" in l for l in errores))  # Cadena de causas
        self.assertTrue(any("INICIO DE LA SIMULACIÓN" in l for l in lineas))
        self.assertTrue(any("FIN DE LA SIMULACIÓN" in l for l in lineas))


if __name__ == "__main__":  # Solo al ejecutar este archivo directamente
    unittest.main(verbosity=2)
