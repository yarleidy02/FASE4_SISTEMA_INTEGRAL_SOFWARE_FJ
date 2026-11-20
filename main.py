"""Simulación de 15 operaciones de Software FJ (válidas e inválidas)."""
from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from logger import obtener_logger, ARCHIVO_LOG


def titulo(n, texto):
    print(f"\n[{n}] {texto}")


def main():
    log = obtener_logger()
    log.info("===== INICIO DE LA SIMULACIÓN =====")
    g = GestorSoftwareFJ()

    titulo(1, "Cliente válido")
    g.registrar_cliente("ana maría ruiz", "1012345678", "ana@correo.com", "3001234567")
    titulo(2, "Cliente con email inválido")
    g.registrar_cliente("Pedro Gómez", "1098765432", "pedro-correo.com", "3109876543")
    titulo(3, "Cliente con documento no numérico")
    g.registrar_cliente("Luis Pérez", "ABC123", "luis@correo.com", "3201112233")
    titulo(4, "Cliente con documento duplicado")
    g.registrar_cliente("Ana Clon", "1012345678", "clon@correo.com", "3001230000")
    titulo(5, "Segundo cliente válido")
    g.registrar_cliente("Carlos Díaz", "79123456", "carlos@correo.com", "3157778899")

    titulo(6, "Servicios válidos (sala, equipo, asesoría)")
    g.agregar_servicio(ReservaSala, "Sala Ejecutiva", 80000, capacidad=10)
    g.agregar_servicio(AlquilerEquipo, "Videobeam", 25000, stock=3)
    g.agregar_servicio(AsesoriaEspecializada, "Asesoría Python", 120000,
                       especialidad="Programación")
    titulo(7, "Servicio inválido (tarifa negativa)")
    g.agregar_servicio(ReservaSala, "Sala Rota", -5, capacidad=4)
    titulo(8, "Servicio inválido (falta un parámetro)")
    g.agregar_servicio(AlquilerEquipo, "Portátil", 30000)
    titulo(9, "Servicio no disponible")
    g.agregar_servicio(ReservaSala, "Sala Mantenimiento", 60000,
                       capacidad=6, disponible=False)

    titulo(10, "Reserva exitosa de sala")
    g.crear_reserva(1, 1, 2, personas=8)
    titulo(11, "Reserva exitosa de equipo (2 unidades)")
    g.crear_reserva(2, 2, 3, cantidad=2)
    titulo(12, "Reserva exitosa de asesoría senior")
    g.crear_reserva(1, 3, 1.5, tema="Clases y objetos", senior=True)
    titulo(13, "Reserva fallida: más personas que la capacidad")
    g.crear_reserva(1, 1, 2, personas=50)
    titulo(14, "Reserva fallida: parámetro 'tema' faltante")
    g.crear_reserva(2, 3, 1)
    titulo(15, "Reserva fallida: servicio no disponible")
    g.crear_reserva(1, 4, 2, personas=3)
    titulo(16, "Reserva fallida: cliente inexistente")
    g.crear_reserva(99, 1, 2, personas=3)
    titulo(17, "Reserva fallida: horas negativas")
    g.crear_reserva(1, 2, -4)

    titulo(18, "Cancelar una reserva ya procesada (operación no permitida)")
    g.cancelar_reserva(1)

    titulo(19, "Demostración de costos sobrecargados (Sala, 2 horas)")
    sala = g.servicios[0]
    print(f"  Con IVA por defecto : ${sala.calcular_costo(2):,.2f}")
    print(f"  Sin impuesto        : ${sala.calcular_costo(2, impuesto=0):,.2f}")
    print(f"  Con 10% descuento   : ${sala.calcular_costo(2, descuento=0.10):,.2f}")
    print(f"  Impuesto 5%         : ${sala.calcular_costo_con_impuesto(2, 0.05):,.2f}")

    titulo(20, "Cálculo inconsistente (descuento de 150%)")
    try:
        sala.calcular_costo(2, descuento=1.5)
    except Exception as error:
        log.error("Cálculo inconsistente capturado: %s", error)
        print(f"  ✗ Controlado: {error}")

    print("\nResumen final:")
    print(f"  Clientes: {len(g.clientes)} | Servicios: {len(g.servicios)} "
          f"| Reservas exitosas: {len(g.reservas)}")
    print(f"  El programa terminó sin caerse. Revisa el log en:\n  {ARCHIVO_LOG}")
    log.info("===== FIN DE LA SIMULACIÓN =====")


if __name__ == "__main__":
    main()
