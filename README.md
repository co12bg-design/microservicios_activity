# Plataforma de reservas: arquitectura inicial

Este repositorio es el entregable inicial del ejercicio del PDF. Describe una plataforma de reservas y contiene dos servicios que pueden ejecutarse por separado: `users-service` y `bookings-service`.

Está pensado para aprender. No necesita experiencia previa en programación para seguir el diseño: cada carpeta tiene una responsabilidad y el README explica cómo se relacionan.

## Entregables incluidos

- Diagrama de arquitectura: [`docs/architecture.md`](docs/architecture.md).
- Requisitos del negocio: [`docs/requirements.md`](docs/requirements.md).
- Límites y propiedad de datos de cada servicio: [`docs/architecture.md`](docs/architecture.md).
- Contratos HTTP iniciales: [`docs/contracts.md`](docs/contracts.md).
- Esqueleto ejecutable de usuarios y reservas en `services/`.
- La regla de negocio para rechazar reservas con fechas que se cruzan.

## Servicios

| Servicio | Puerto local | Responsabilidad |
|---|---:|---|
| `users-service` | 8001 | Registrar y consultar perfiles; guardar contraseñas como hashes. |
| `resources-service` | 8003 (diseñado, pendiente de implementar) | Definir habitaciones, sus características, precio y disponibilidad. |
| `bookings-service` | 8002 | Crear y consultar reservas, evitando cruces de fechas. |
| `payments-service` | 8004 (diseñado, pendiente de implementar) | Administrar métodos y operaciones de pago, y registrar sus resultados. |
| `notifications-service` | 8005 (diseñado, pendiente de implementar) | Avisar por correo y SMS sobre pagos exitosos, fecha de llegada y actualizaciones de reserva. |

Los servicios implementados guardan datos en memoria. Esto permite explorar sus endpoints sin instalar una base de datos, pero los datos se borran al reiniciar el servicio. La persistencia real y el despliegue quedan para una siguiente etapa.

## Cómo iniciar

Necesitas Python 3.11 o superior y [uv](https://docs.astral.sh/uv/).

Inicia primero los usuarios y luego las reservas, cada uno en una terminal distinta. Reservas consulta al servicio de usuarios para comprobar que el ID corresponda a una persona registrada:

```bash
cd services/users-service
uv run fastapi dev app/main.py --port 8001
```

```bash
cd services/bookings-service
uv run fastapi dev app/main.py --port 8002
```

Para cambiar la dirección de `users-service`, configura `USERS_SERVICE_URL` antes de iniciar reservas. Si el servicio de usuarios no está disponible, la creación de la reserva se detiene de forma segura.

FastAPI muestra una documentación interactiva en `http://127.0.0.1:8001/docs` y `http://127.0.0.1:8002/docs`. Desde ahí puedes probar los endpoints con formularios, sin escribir código para enviar las peticiones.

## Cómo entender una solicitud

Cuando una persona crea una reserva, la petición entra por `presentation` (HTTP), pasa a `application` (caso de uso), aplica la regla del dominio y consulta el repositorio. Por ahora, `infrastructure` implementa ese repositorio usando una lista en memoria.

```text
Petición HTTP → Presentation → Application → Domain
                                      ↓
                               Infrastructure → datos
```

El dominio no conoce FastAPI ni cómo se guardan los datos. Así se puede cambiar la forma de guardar información sin reescribir la regla de reservas.

## Decisión importante sobre las fechas

Una reserva ocupa las noches desde la fecha de llegada hasta antes de la fecha de salida. Así, una reserva que termina el 10 de junio y otra que empieza el 10 de junio pueden compartir ese día de cambio. Para la misma habitación, sí hay conflicto cuando `nueva_llegada < existente_salida` y `nueva_salida > existente_llegada`.

Por ejemplo, del 8 al 11 se cruza con una reserva del 10 al 12, pero no con una del 11 al 14.

## Estado del entregable

Este es un punto de partida educativo: dos servicios ejecutables, contratos pequeños y arquitectura documentada. El almacenamiento todavía no es persistente; tampoco están implementados los servicios de recursos, pagos y notificaciones. Esas decisiones quedan explícitas para que el sistema pueda evolucionar sin fingir que ya está completo.
