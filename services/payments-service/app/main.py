from fastapi import FastAPI, HTTPException, status

from app.application.process_payment import ProcessPayment
from app.domain.entities import Payment
from app.infrastructure.memory_payment_repository import MemoryPaymentRepository
from app.presentation.schemas import PaymentResponse, ProcessPaymentRequest

app = FastAPI(title="Payments Service", version="0.1.0")
repository = MemoryPaymentRepository()
process_payment = ProcessPayment(repository)


@app.get("/payment-methods")
def list_payment_methods() -> list[str]:
    return ["CARD", "CASH", "BANK_TRANSFER"]


@app.post("/payments", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def post_payment(request: ProcessPaymentRequest) -> Payment:
    try:
        return process_payment.execute(
            booking_id=request.booking_id,
            method=request.method,
            amount=request.amount,
            currency=request.currency,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.get("/payments", response_model=list[PaymentResponse])
def list_payments() -> list[Payment]:
    return repository.list_all()
