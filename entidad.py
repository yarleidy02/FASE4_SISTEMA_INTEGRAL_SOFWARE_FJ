"""Clase abstracta que representa cualquier entidad general del sistema."""
from abc import ABC, abstractmethod


class Entidad(ABC):
    """Base de Cliente, Servicio y Reserva. No se puede instanciar directamente."""

    def __init__(self, identificador: int):
        self._id = identificador  # atributo "protegido" (encapsulación)

    @property
    def id(self) -> int:
        """Solo lectura: el id no se puede cambiar desde fuera."""
        return self._id

    @abstractmethod
    def describir(self) -> str:
        """Cada entidad debe saber describirse (polimorfismo)."""
