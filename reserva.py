"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidad import Entidad
from cliente import Cliente
from servicios import Servicio
from excepciones import (ReservaInvalidaError, OperacionNoPermitidaError,
                         ServicioNoDisponibleError, ErrorSoftwareFJ,
                         ServicioInvalidoError, ParametroFaltanteError)
from logger import obtener_logger

log = obtener_logger()

PENDIENTE, CONFIRMADA, PROCESADA, CANCELADA = (
    "PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")


class Reserva(Entidad):
    def __init__(self, identificador: int, cliente: Cliente, servicio: Servicio,
                 horas: float, **extra):
        super().__init__(identificador)
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva necesita un cliente válido.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva necesita un servicio válido.")
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._extra = extra          # parámetros propios de cada servicio
        self._estado = PENDIENTE
        self._costo_total = None

    @property
    def estado(self) -> str:
        return self._estado

    @property
    def costo_total(self):
        return self._costo_total

    def confirmar(self) -> None:
        """PENDIENTE -> CONFIRMADA (valida parámetros y disponibilidad)."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva en estado {self._estado}.")
        try:
            if not self._servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"'{self._servicio.nombre}' no está disponible.")
            self._servicio.validar_parametros(self._horas, **self._extra)
        except (ServicioInvalidoError, ParametroFaltanteError) as error:
            # Encadenamiento de excepciones: "raise ... from error"
            raise ReservaInvalidaError(
                f"Reserva #{self.id} rechazada: {error}") from error
        else:
            self._estado = CONFIRMADA   # solo si NO hubo error
            log.info("Reserva #%s confirmada.", self.id)
        finally:
            log.info("Intento de confirmación de reserva #%s finalizado.", self.id)

    def cancelar(self) -> None:
        if self._estado in (CANCELADA, PROCESADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado}.")
        self._estado = CANCELADA
        log.info("Reserva #%s cancelada.", self.id)

    def procesar(self, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """CONFIRMADA -> PROCESADA, calculando el costo final."""
        if self._estado != CONFIRMADA:
            raise OperacionNoPermitidaError(
                f"Solo se procesan reservas CONFIRMADAS (actual: {self._estado}).")
        try:
            # Parámetros opcionales según el tipo de servicio (polimorfismo)
            opciones = {k: v for k, v in self._extra.items()
                        if k in ("cantidad", "senior")}
            self._costo_total = self._servicio.calcular_costo(
                self._horas, impuesto, descuento, **opciones)
        except ErrorSoftwareFJ as error:
            raise ReservaInvalidaError(
                f"No se pudo procesar la reserva #{self.id}") from error
        else:
            self._estado = PROCESADA
            log.info("Reserva #%s procesada. Total: $%s", self.id, self._costo_total)
            return self._costo_total
        finally:
            log.info("Fin de procesamiento de reserva #%s.", self.id)

    def describir(self) -> str:
        total = f"${self._costo_total:,.2f}" if self._costo_total is not None else "-"
        return (f"Reserva #{self.id} | {self._cliente.nombre} | "
                f"{self._servicio.nombre} | {self._horas}h | {self._estado} | {total}")
