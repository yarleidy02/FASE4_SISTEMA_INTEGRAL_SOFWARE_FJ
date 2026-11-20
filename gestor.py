"""Gestor central: guarda todo en listas (sin base de datos) y protege
al programa de errores: cada operación captura y registra su excepción."""
from cliente import Cliente
from servicios import Servicio
from reserva import Reserva
from excepciones import ErrorSoftwareFJ, ClienteInvalidoError, ServicioInvalidoError
from logger import obtener_logger

log = obtener_logger()


class GestorSoftwareFJ:
    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def _siguiente_id(self, lista) -> int:
        return len(lista) + 1

    def registrar_cliente(self, nombre, documento, email, telefono):
        try:
            if any(c.documento == str(documento).strip() for c in self.clientes):
                raise ClienteInvalidoError(f"Documento {documento} ya registrado.")
            cliente = Cliente(self._siguiente_id(self.clientes),
                              nombre, documento, email, telefono)
        except ErrorSoftwareFJ as error:
            log.error("Registro de cliente fallido: %s", error)
            print(f"  ✗ Cliente NO registrado: {error}")
            return None
        else:
            self.clientes.append(cliente)
            log.info("Cliente registrado: %s", cliente.describir())
            print(f"  ✓ {cliente.describir()}")
            return cliente

    def agregar_servicio(self, clase_servicio, *args, **kwargs):
        """Crea cualquier servicio: clase_servicio puede ser Sala, Equipo, Asesoría."""
        try:
            servicio = clase_servicio(self._siguiente_id(self.servicios), *args, **kwargs)
        except (ErrorSoftwareFJ, TypeError) as error:   # TypeError = argumentos faltantes
            log.error("Creación de servicio fallida: %s", error)
            print(f"  ✗ Servicio NO creado: {error}")
            return None
        else:
            self.servicios.append(servicio)
            log.info("Servicio creado: %s", servicio.describir())
            print(f"  ✓ {servicio.describir()}")
            return servicio

    def _buscar(self, lista, identificador, excepcion, etiqueta):
        for item in lista:
            if item.id == identificador:
                return item
        raise excepcion(f"{etiqueta} #{identificador} no existe.")

    def crear_reserva(self, id_cliente, id_servicio, horas, **extra):
        try:
            cliente = self._buscar(self.clientes, id_cliente, ClienteInvalidoError, "Cliente")
            servicio = self._buscar(self.servicios, id_servicio, ServicioInvalidoError, "Servicio")
            reserva = Reserva(self._siguiente_id(self.reservas),
                              cliente, servicio, horas, **extra)
            reserva.confirmar()
            reserva.procesar()
        except ErrorSoftwareFJ as error:
            log.error("Reserva fallida: %s | causa: %r", error, error.__cause__)
            print(f"  ✗ Reserva fallida: {error}")
            return None
        else:
            self.reservas.append(reserva)
            print(f"  ✓ {reserva.describir()}")
            return reserva

    def cancelar_reserva(self, id_reserva):
        try:
            reserva = self._buscar(self.reservas, id_reserva, ErrorSoftwareFJ, "Reserva")
            reserva.cancelar()
        except ErrorSoftwareFJ as error:
            log.error("Cancelación fallida: %s", error)
            print(f"  ✗ Cancelación fallida: {error}")
        else:
            print(f"  ✓ {reserva.describir()}")
