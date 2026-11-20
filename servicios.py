"""Clase abstracta Servicio y tres servicios especializados."""
from abc import ABC, abstractmethod
import math

from entidad import Entidad
from excepciones import (ServicioInvalidoError, ParametroFaltanteError,
                         CalculoInconsistenteError)

IVA = 0.19  # impuesto por defecto


class Servicio(Entidad, ABC):
    def __init__(self, identificador: int, nombre: str, tarifa_hora: float,
                 disponible: bool = True):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioInvalidoError("El servicio necesita un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_hora = float(tarifa_hora)
        self._disponible = bool(disponible)

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    @disponible.setter
    def disponible(self, valor: bool):
        self._disponible = bool(valor)

    # ---- métodos que cada servicio DEBE sobrescribir ----
    @abstractmethod
    def costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos."""

    @abstractmethod
    def validar_parametros(self, horas: float, **extra) -> None:
        """Lanza excepción si los parámetros de la reserva no son válidos."""

    # ---- método "sobrecargado" (en Python: parámetros opcionales) ----
    def calcular_costo(self, horas: float, impuesto: float = IVA,
                       descuento: float = 0.0) -> float:
        """Variantes de uso:
        calcular_costo(2)                      -> con IVA por defecto
        calcular_costo(2, impuesto=0)          -> sin impuesto
        calcular_costo(2, descuento=0.10)      -> con IVA y 10% de descuento
        calcular_costo(2, 0.05, 0.10)          -> impuesto y descuento propios
        """
        if not (0 <= descuento < 1) or impuesto < 0:
            raise CalculoInconsistenteError("Impuesto o descuento fuera de rango.")
        total = self.costo_base(horas) * (1 - descuento) * (1 + impuesto)
        if math.isnan(total) or total < 0:
            raise CalculoInconsistenteError(f"Costo inconsistente: {total}")
        return round(total, 2)

    def calcular_costo_con_impuesto(self, horas: float, impuesto: float) -> float:
        """Segunda variante explícita: solo impuesto, sin descuento."""
        return self.calcular_costo(horas, impuesto=impuesto, descuento=0.0)

    def describir(self) -> str:
        estado = "disponible" if self._disponible else "NO disponible"
        return f"{self._nombre} - ${self._tarifa_hora:,.0f}/hora ({estado})"

    @staticmethod
    def _validar_horas(horas) -> None:
        if not isinstance(horas, (int, float)) or horas <= 0 or horas > 12:
            raise ServicioInvalidoError("Las horas deben estar entre 0 y 12.")


class ReservaSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, capacidad: int,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo.")
        self._capacidad = capacidad

    def costo_base(self, horas):
        return self._tarifa_hora * horas

    def validar_parametros(self, horas, **extra):
        self._validar_horas(horas)
        personas = extra.get("personas")
        if personas is None:
            raise ParametroFaltanteError("Falta el parámetro 'personas'.")
        if not isinstance(personas, int) or not (0 < personas <= self._capacidad):
            raise ServicioInvalidoError(
                f"Personas debe estar entre 1 y {self._capacidad}.")

    def describir(self):
        return f"[Sala] {super().describir()} - capacidad {self._capacidad}"


class AlquilerEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_hora, stock: int,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(stock, int) or stock <= 0:
            raise ServicioInvalidoError("El stock debe ser un entero positivo.")
        self._stock = stock

    def costo_base(self, horas):
        return self._tarifa_hora * horas  # se multiplica por cantidad en la reserva

    def validar_parametros(self, horas, **extra):
        self._validar_horas(horas)
        cantidad = extra.get("cantidad", 1)
        if not isinstance(cantidad, int) or not (0 < cantidad <= self._stock):
            raise ServicioInvalidoError(f"Cantidad debe estar entre 1 y {self._stock}.")

    def calcular_costo(self, horas, impuesto=IVA, descuento=0.0, cantidad: int = 1):
        """Sobrescribe el método base agregando el parámetro 'cantidad'."""
        return round(super().calcular_costo(horas, impuesto, descuento) * cantidad, 2)

    def describir(self):
        return f"[Equipo] {super().describir()} - stock {self._stock}"


class AsesoriaEspecializada(Servicio):
    RECARGO_SENIOR = 1.5

    def __init__(self, identificador, nombre, tarifa_hora, especialidad: str,
                 disponible=True):
        super().__init__(identificador, nombre, tarifa_hora, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ServicioInvalidoError("La asesoría requiere una especialidad.")
        self._especialidad = especialidad.strip()

    def costo_base(self, horas):
        return self._tarifa_hora * horas

    def validar_parametros(self, horas, **extra):
        self._validar_horas(horas)
        if not extra.get("tema"):
            raise ParametroFaltanteError("Falta el parámetro 'tema' de la asesoría.")

    def calcular_costo(self, horas, impuesto=IVA, descuento=0.0, senior: bool = False):
        base = super().calcular_costo(horas, impuesto, descuento)
        return round(base * self.RECARGO_SENIOR, 2) if senior else base

    def describir(self):
        return f"[Asesoría] {super().describir()} - {self._especialidad}"
