# Plataforma de reservas: arquitectura inicial

Este repositorio es el entregable del ejercicio del PDF. Describe una plataforma de reservas y contiene cinco servicios ejecutables de demostración.

Está pensado para aprender. No necesita experiencia previa en programación para seguir el diseño: cada carpeta tiene una responsabilidad y el README explica cómo se relacionan.

## Entregables incluidos

- Diagrama de arquitectura: [`docs/architecture.md`](docs/architecture.md).
- Requisitos del negocio: [`docs/requirements.md`](docs/requirements.md).
- Límites y propiedad de datos de cada servicio: [`docs/architecture.md`](docs/architecture.md).
- Contratos HTTP iniciales: [`docs/contracts.md`](docs/contracts.md).
- Esqueleto ejecutable de los cinco servicios en `services/`.
- La regla de negocio para rechazar reservas con fechas que se cruzan.

## Servicios

| Servicio | Puerto local | Responsabilidad |
|---|---:|---|
| `users-service` | 8001 | Registrar y consultar perfiles; guardar contraseñas como hashes. |
| `resources-service` | 8003 | Mostrar habitaciones de demostración, sus características y precio por noche. |
| `bookings-service` | 8002 | Crear y consultar reservas, evitando cruces de fechas. |
| `payments-service` | 8004 | Simular un pago, registrar el método y devolver el resultado. |
| `notifications-service` | 8005 | Crear avisos simulados por correo y SMS. |

Los cinco servicios guardan datos en memoria. Esto permite explorar sus endpoints sin instalar una base de datos, pero los datos se borran al reiniciarlos. Los pagos no cobran dinero real y las notificaciones no se envían por internet: quedan registradas para que puedas verlas en el servicio.

## Cómo iniciar

Necesitas Python 3.11 o superior y [uv](https://docs.astral.sh/uv/).

Inicia cada servicio en una terminal distinta. Abre cinco terminales en la carpeta indicada y ejecuta estos comandos, uno por terminal:

```bash
cd services/users-service
uv run fastapi dev app/main.py --port 8001
```

```bash
cd services/resources-service
uv run fastapi dev app/main.py --port 8003
```

```bash
cd services/payments-service
uv run fastapi dev app/main.py --port 8004
```

```bash
cd services/notifications-service
uv run fastapi dev app/main.py --port 8005
```

```bash
cd services/bookings-service
uv run fastapi dev app/main.py --port 8002
```

Abre las terminales e inicia los servicios en este orden: usuarios, habitaciones, pagos, notificaciones y reservas. Reservas consulta los otros cuatro servicios. Si alguno no está disponible, no completa la solicitud.

FastAPI muestra una documentación interactiva en `http://127.0.0.1:8001/docs` y `http://127.0.0.1:8002/docs`. Desde ahí puedes probar los endpoints con formularios, sin escribir código para enviar las peticiones.

También puedes abrir la documentación de habitaciones en `http://127.0.0.1:8003/docs`, pagos en `http://127.0.0.1:8004/docs` y notificaciones en `http://127.0.0.1:8005/docs`.

## Probar una reserva de principio a fin

1. En Usuarios (`8001/docs`), crea un usuario con `POST /users` y copia el `id` que devuelve.
2. En Habitaciones (`8003/docs`), consulta `GET /rooms` y copia el ID de una habitación demo.
3. En Reservas (`8002/docs`), crea una reserva con `POST /bookings`, usando esos dos IDs y fechas futuras.
4. La respuesta muestra el valor calculado, el pago simulado y el estado `CONFIRMED`.
5. En Pagos (`8004/docs`), `GET /payments` muestra el pago simulado. En Notificaciones (`8005/docs`), `GET /notifications` muestra los avisos de correo y SMS que quedaron registrados.

Las habitaciones demo son una habitación estándar a COP 180.000 por noche y una habitación familiar a COP 250.000 por noche. No se realiza ningún cobro ni envío real.

## Cómo entender una solicitud

Cuando una persona crea una reserva, `bookings-service` verifica el usuario en Usuarios, obtiene habitación y precio de Habitaciones, evita cruces de fechas, calcula el valor, pide el pago a Pagos y registra avisos en Notificaciones. Dentro de cada servicio, la petición entra por `presentation`, pasa a `application`, aplica reglas de `domain` y usa `infrastructure` para comunicarse o guardar datos.

```text
Petición HTTP → Presentation → Application → Domain
                                      ↓
                               Infrastructure → datos/servicios
```

El dominio no conoce FastAPI ni cómo se guardan los datos. Así se puede cambiar la forma de guardar información sin reescribir la regla de reservas.

## Decisión importante sobre las fechas

Una reserva ocupa las noches desde la fecha de llegada hasta antes de la fecha de salida. Así, una reserva que termina el 10 de junio y otra que empieza el 10 de junio pueden compartir ese día de cambio. Para la misma habitación, sí hay conflicto cuando `nueva_llegada < existente_salida` y `nueva_salida > existente_llegada`.

Por ejemplo, del 8 al 11 se cruza con una reserva del 10 al 12, pero no con una del 11 al 14.

## Estado del entregable

Este es un punto de partida educativo con cinco servicios ejecutables y comunicados para una reserva de demostración. Aún no usa una base de datos, un proveedor de pagos real ni un proveedor de correo/SMS real.
