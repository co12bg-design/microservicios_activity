# Contratos iniciales entre servicios

Un contrato es un acuerdo sobre qué datos se envían y qué respuesta se espera. Un servicio conoce el contrato público de otro servicio, pero no importa sus clases internas.

## Contratos implementados

### Crear usuario — `users-service`

`POST /users`

Entrada:

```json
{
  "name": "Ana Pérez",
  "email": "ana@example.com",
  "phone_number": "+573001112233",
  "password": "ejemplo-seguro-123"
}
```

Respuesta `201 Created`:

```json
{
  "id": "c7f817af-c99e-4e5a-92f8-55a34544c64d",
  "name": "Ana Pérez",
  "email": "ana@example.com",
  "phone_number": "+573001112233"
}
```

Consultar usuario: `GET /users/{user_id}`. Devuelve `200 OK` o `404 Not Found`.

El perfil inicial contiene nombre, correo y teléfono en formato internacional. La contraseña se convierte en un hash antes de guardarse y no aparece en la respuesta. El inicio de sesión queda para una siguiente etapa.

Las reservas requieren un `user_id` existente. `bookings-service` consulta `GET /users/{user_id}` en `users-service`: si no existe, rechaza la reserva; si usuarios no responde, devuelve un error temporal y no la crea.

### Crear reserva — `bookings-service`

`POST /bookings`

Entrada:

```json
{
  "user_id": "c7f817af-c99e-4e5a-92f8-55a34544c64d",
  "room_id": "041c3bf2-b374-4728-b4c5-963d82fb2a7b",
  "start_date": "2026-11-10",
  "end_date": "2026-11-12",
  "payment_method": "CARD",
  "total_amount": "250.00"
}
```

Respuesta `201 Created`: identificador de reserva, los identificadores y fechas, forma de pago, valor, hora de creación y estado `PENDING`.

Consultar reserva: `GET /bookings/{booking_id}`. Devuelve `200 OK` o `404 Not Found`. Las fechas deben ser fechas de calendario válidas; la llegada no puede estar en el pasado, no puede superar seis meses desde hoy y la salida debe ser posterior a la llegada. Si las fechas se cruzan con otra reserva del mismo recurso, la creación responde `409 Conflict`.

`payment_method` admite `CARD`, `CASH` o `BANK_TRANSFER` como opciones iniciales. `payments-service` será dueño de los métodos disponibles y del procesamiento; `bookings-service` solo registra cuál eligió la persona. El monto es una copia del precio acordado al reservar. En un sistema completo, `bookings-service` debe pedir el precio a `resources-service`; no debe confiar en un monto enviado por el navegador. En este esqueleto el monto se recibe en la solicitud como simplificación educativa.

## Identificadores y propiedad

`user_id` y `room_id` son UUID. Reservas guarda esos identificadores para referirse a un usuario y a una habitación; no copia ni comparte sus modelos internos. En el esqueleto, `user_id` sí se valida consultando a `users-service`; `room_id` todavía no se valida contra `resources-service` porque ese servicio está pendiente.

## Contratos previstos para siguientes etapas

- `resources-service`: `GET /rooms/{room_id}` para consultar una habitación, su precio y disponibilidad.
- `payments-service`: recibe una solicitud de pago con `booking_id`, valor y método elegido; publica `PaymentSucceeded` o `PaymentFailed` con el resultado.
- `bookings-service`: escucha el resultado del pago y actualiza el estado de la reserva. Un pago exitoso puede llevarla a `CONFIRMED`.
- `notifications-service`: escucha `PaymentSucceeded` y `BookingUpdated`, obtiene correo y teléfono usando `user_id`, y envía ambos avisos. Incluye confirmación del pago, fecha de llegada (check-in), estado de la reserva y cualquier cambio.

Estos mensajes y contratos de servicios son planeados para una siguiente etapa; aún no existe el envío real de correo/SMS ni la integración con pagos. Antes de agregar más campos o estados, se deben acordar con los servicios que los consumen.
