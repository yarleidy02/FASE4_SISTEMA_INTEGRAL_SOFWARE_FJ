"""Excepciones personalizadas de Software FJ.

Todas heredan de ErrorSoftwareFJ, así podemos capturar "cualquier error
propio del sistema" con un solo except, o uno específico si lo necesitamos.
"""


class ErrorSoftwareFJ(Exception):
    """Excepción base del sistema."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Datos del cliente inválidos o cliente inexistente."""


class ServicioInvalidoError(ErrorSoftwareFJ):
    """Datos o parámetros del servicio inválidos."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Falta un parámetro obligatorio."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """El servicio existe pero no está disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """La reserva no se pudo crear o procesar."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Operación no permitida para el estado actual (p. ej. cancelar dos veces)."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """El cálculo de costos dio un resultado imposible (negativo, NaN, etc.)."""
