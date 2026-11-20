"""Configuración del archivo de logs (único uso de archivos permitido)."""
import logging
import os

RUTA_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
ARCHIVO_LOG = os.path.join(RUTA_LOG, "software_fj.log")


def obtener_logger() -> logging.Logger:
    """Devuelve el logger del sistema (se configura una sola vez)."""
    logger = logging.getLogger("software_fj")
    if not logger.handlers:  # evita duplicar mensajes si se llama varias veces
        os.makedirs(RUTA_LOG, exist_ok=True)
        logger.setLevel(logging.INFO)
        manejador = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
        manejador.setFormatter(
            logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
        )
        logger.addHandler(manejador)
    return logger
