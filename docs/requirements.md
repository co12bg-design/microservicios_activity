# Requisitos del sistema de reservas

Este documento dice **qué debe hacer** la aplicación. El diagrama y los contratos explican después cómo se organizan y se comunican sus partes.

## Requisitos funcionales

1. Una persona puede registrarse con nombre, correo, teléfono y contraseña. La contraseña se guarda protegida como hash; nunca se devuelve ni se guarda como texto legible.
2. Solo una persona registrada puede crear una reserva.
3. La persona puede elegir una habitación y una fecha de ingreso y salida.
4. Las fechas deben existir en el calendario. La llegada no puede ser anterior a hoy ni estar a más de seis meses calendario desde hoy. La fecha de salida debe ser posterior a la llegada.
5. No se puede reservar una habitación si sus fechas se cruzan con otra reserva que esté pendiente o confirmada. La fecha de salida es exclusiva: una nueva llegada ese mismo día no cuenta como cruce.
6. Cada reserva conserva la habitación, fechas de ingreso y salida, forma de pago elegida, valor acordado, estado y hora de creación.
7. `payments-service` administra los métodos y las operaciones de pago, y comunica si un pago fue exitoso o falló. Los datos completos de tarjetas no se guardan en la reserva.
8. Después de un pago exitoso, la persona recibe una confirmación por correo y SMS. También recibe avisos por ambos canales cuando se actualiza la reserva.
9. Las notificaciones incluyen la fecha de llegada (check-in), el estado de la reserva y la actualización ocurrida.

## Requisitos de arquitectura

- `users-service` es dueño del perfil y las credenciales.
- `resources-service` es dueño de las habitaciones, sus características y su precio.
- `bookings-service` es dueño de las reservas y evita los conflictos de fechas.
- `payments-service` es dueño de métodos y operaciones de pago.
- `notifications-service` es dueño de la entrega de mensajes por correo y SMS.
- Cada servicio tiene sus propias capas de Clean Architecture. Un servicio no comparte con otro sus clases internas ni modelos de base de datos.

## Cómo sabremos que la primera entrega cubre el ejercicio

- Hay un diagrama que muestra los cinco servicios y sus comunicaciones.
- La responsabilidad y propiedad de datos de cada servicio está explicada.
- Existe una estructura Clean Architecture para `users-service` y `bookings-service`.
- Los contratos de registro y creación de reserva describen entradas, respuestas y errores principales.
- La regla de cruce de fechas está descrita y aparece en el código del esqueleto de reservas.
- El README identifica qué funciona ahora y qué queda diseñado para una siguiente etapa.

## Alcance del esqueleto actual

El código de esta entrega registra usuarios, protege sus contraseñas con un hash, verifica que el usuario exista y crea reservas en memoria. También impide fechas pasadas, llegadas a más de seis meses y cruces con reservas existentes. El servicio de habitaciones, los pagos reales, los mensajes de correo/SMS y una base de datos persistente están descritos, pero pendientes de implementación.
