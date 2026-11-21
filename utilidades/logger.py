# Archivo: utilidades/logger.py
# Registra en un archivo de texto todos los eventos y errores del sistema.

import logging  # Módulo estándar de Python para escribir registros (logs)
import os  # Permite trabajar con rutas y carpetas del sistema operativo

# Carpeta raíz del proyecto (un nivel por encima de "utilidades")
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Carpeta donde se guardará el archivo de logs (las pruebas pueden cambiarla
# con la variable de entorno SOFTWARE_FJ_LOG_DIR para no tocar el log real)
RUTA_LOGS = os.environ.get("SOFTWARE_FJ_LOG_DIR", os.path.join(RAIZ_PROYECTO, "logs"))
# Ruta completa del archivo de logs
ARCHIVO_LOG = os.path.join(RUTA_LOGS, "software_fj.log")


def _configurar_logger():
    """Crea y configura el logger que escribe en el archivo de logs."""
    os.makedirs(RUTA_LOGS, exist_ok=True)  # Crea la carpeta logs si no existe
    logger = logging.getLogger("software_fj")  # Obtiene el logger del sistema
    if logger.handlers:  # Si ya fue configurado antes...
        return logger  # ...lo reutiliza para no duplicar los registros
    logger.setLevel(logging.INFO)  # Registra desde el nivel INFO hacia arriba
    manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")  # Archivo
    formato = logging.Formatter(  # Define cómo se ve cada línea del log
        "%(asctime)s | %(levelname)s | %(message)s"
    )
    manejador.setFormatter(formato)  # Aplica el formato al archivo
    logger.addHandler(manejador)  # Conecta el archivo al logger
    logger.propagate = False  # Evita que se imprima también en consola
    return logger  # Devuelve el logger listo para usar


_logger = _configurar_logger()  # Se configura una sola vez al importar


def registrar_evento(mensaje):
    """Registra un evento normal del sistema (nivel INFO)."""
    _logger.info(mensaje)  # Escribe el mensaje en el archivo


def registrar_error(mensaje, excepcion=None):
    """Registra un error (nivel ERROR) y la cadena de causas si existe."""
    if excepcion is not None:  # Si se recibió la excepción capturada...
        mensaje += f" | {type(excepcion).__name__}: {excepcion}"  # Agrega tipo
        causa = excepcion.__cause__  # Revisa si hay una excepción encadenada
        while causa is not None:  # Recorre toda la cadena de causas
            mensaje += f" | causa: {type(causa).__name__}: {causa}"  # La anota
            causa = causa.__cause__  # Pasa a la siguiente causa
    _logger.error(mensaje)  # Escribe el error en el archivo


def registrar_critico(mensaje, excepcion=None):
    """Registra un error inesperado."""
    if excepcion is not None:  # Si se recibió la excepción capturada.

        mensaje += f" | {type(excepcion).__name__}: {excepcion}"  # Agrega tipo
    _logger.critical(mensaje)  # Escribe el error crítico en el archivo
