from fastapi import FastAPI, HTTPException, status

from app.application.create_user import CreateUser
from app.domain.entities import User
from app.infrastructure.memory_user_repository import MemoryUserRepository
from app.infrastructure.scrypt_password_hasher import ScryptPasswordHasher
from app.presentation.schemas import CreateUserRequest, UserResponse

app = FastAPI(title="Users Service", version="0.1.0")
repository = MemoryUserRepository()
create_user = CreateUser(repository, ScryptPasswordHasher())


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def post_user(request: CreateUserRequest) -> User:
    try:
        return create_user.execute(
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
            password=request.password,
        )
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str) -> User:
    user = repository.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return user
