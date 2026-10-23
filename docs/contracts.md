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
  "room_id": "11111111-1111-4111-8111-111111111111",
  "start_date": "2026-11-10",
  "end_date": "2026-11-12",
  "payment_method": "CARD"
}
```

Respuesta `201 Created`: identificador de reserva, los identificadores y fechas, forma de pago, valor calculado desde el precio de la habitación, moneda, identificador del pago, hora de creación y estado. En esta demo, el pago resulta exitoso y la reserva queda `CONFIRMED`.

Consultar reserva: `GET /bookings/{booking_id}`. Devuelve `200 OK` o `404 Not Found`. Las fechas deben ser fechas de calendario válidas; la llegada no puede estar en el pasado, no puede superar seis meses desde hoy y la salida debe ser posterior a la llegada. Si las fechas se cruzan con otra reserva del mismo recurso, la creación responde `409 Conflict`.

`payment_method` admite `CARD`, `CASH` o `BANK_TRANSFER`. `payments-service` mantiene la lista de métodos y simula el resultado del pago. No se envían datos reales de tarjeta ni se realiza un cobro real. `bookings-service` obtiene el precio por noche de `resources-service` y lo multiplica por el número de noches; el navegador no envía el monto.

## Identificadores y propiedad

`user_id` y `room_id` son UUID. Reservas guarda esos identificadores para referirse a un usuario y a una habitación; no copia ni comparte sus modelos internos. Antes de reservar, consulta al servicio de usuarios y al de habitaciones para comprobar que ambos identificadores existen.

## Contratos de los otros tres servicios

- `resources-service`: `GET /rooms` lista habitaciones de demostración; `GET /rooms/{room_id}` devuelve su nombre, hotel, precio por noche, moneda y estado.
- `payments-service`: `GET /payment-methods` muestra métodos; `POST /payments` registra un pago simulado por `booking_id`, método, valor y moneda; `GET /payments` permite revisar los resultados.
- `notifications-service`: `POST /notifications` registra dos avisos simulados, uno por correo y otro por SMS, con el estado y la fecha de llegada; `GET /notifications` permite revisarlos.

Durante una reserva, `bookings-service` llama a estos servicios por HTTP. El aviso incluye confirmación del pago exitoso, la fecha de llegada (check-in), el estado y cualquier actualización. Los mensajes quedan registrados localmente; no se envían por proveedores de correo/SMS.
