# Software FJ – Gestión de Clientes, Servicios y Reservas

Proyecto de Programación (UNAD, curso 213023) con POO y manejo de excepciones, sin bases de datos.

## Ejecutar
    python main.py

## Estructura
- `entidad.py`: clase abstracta base.
- `cliente.py`: Cliente con validaciones y encapsulación.
- `servicios.py`: Servicio (abstracta) + ReservaSala, AlquilerEquipo, AsesoriaEspecializada.
- `reserva.py`: Reserva (confirmar, cancelar, procesar).
- `excepciones.py`: excepciones personalizadas.
- `logger.py`: configuración del archivo de logs (`logs/software_fj.log`).
- `gestor.py`: listas internas y operaciones protegidas con try/except.
- `main.py`: simulación de 20 operaciones.
