from fastapi import FastAPI
from app.api import routers
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
)

# Incluir los routers de la API
app.include_router(routers.auth_router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(routers.users_router, prefix="/api/v1/users", tags=["Users"])
# Aquí se incluirán más routers a medida que se desarrollen para cada módulo
# app.include_router(routers.patients_router, prefix="/api/v1/patients", tags=["Patients"])
# app.include_router(routers.appointments_router, prefix="/api/v1/appointments", tags=["Appointments"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Ophthalmological Clinic API!"}