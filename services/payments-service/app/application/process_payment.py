from decimal import Decimal
from uuid import UUID

from app.domain.entities import Payment, PaymentMethod
from app.domain.repositories import PaymentRepository


class ProcessPayment:
    """Ejercicio: registra un resultado simulado; no cobra dinero real."""

    def __init__(self, repository: PaymentRepository) -> None:
        self.repository = repository

    def execute(
        self, booking_id: UUID, method: PaymentMethod, amount: Decimal, currency: str
    ) -> Payment:
        existing = self.repository.get_by_booking(booking_id)
        if existing is not None:
            return existing
        if amount <= 0:
            raise ValueError("El valor del pago debe ser mayor que cero")
        payment = Payment.simulated_success(booking_id, method, amount, currency)
        self.repository.add(payment)
        return payment
