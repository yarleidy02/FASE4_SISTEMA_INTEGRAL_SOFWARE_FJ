"""Clase Cliente con validaciones robustas y datos personales encapsulados."""
import re

from entidad import Entidad
from excepciones import ClienteInvalidoError

_PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


class Cliente(Entidad):
    def __init__(self, identificador: int, nombre: str, documento: str,
                 email: str, telefono: str):
        super().__init__(identificador)
        # Se asigna mediante los setters, que validan cada dato.
        self.nombre = nombre
        self.documento = documento
        self.email = email
        self.telefono = telefono

    # ---- nombre ----
    @property
    def nombre(self) -> str:
        return self.__nombre  # atributo privado (name mangling)

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ClienteInvalidoError("El nombre debe tener al menos 3 caracteres.")
        self.__nombre = valor.strip().title()

    # ---- documento ----
    @property
    def documento(self) -> str:
        return self.__documento

    @documento.setter
    def documento(self, valor: str):
        valor = str(valor).strip()
        if not valor.isdigit() or not (6 <= len(valor) <= 12):
            raise ClienteInvalidoError(
                "El documento debe ser numérico, de 6 a 12 dígitos.")
        self.__documento = valor

    # ---- email ----
    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str) or not _PATRON_EMAIL.match(valor.strip()):
            raise ClienteInvalidoError(f"Email inválido: {valor!r}")
        self.__email = valor.strip().lower()

    # ---- teléfono ----
    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        valor = str(valor).strip()
        if not valor.isdigit() or len(valor) != 10:
            raise ClienteInvalidoError("El teléfono debe tener 10 dígitos numéricos.")
        self.__telefono = valor

    def describir(self) -> str:
        return f"Cliente #{self.id}: {self.nombre} (doc. {self.documento})"
