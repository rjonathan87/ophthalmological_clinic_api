# Documentación API Clínica Oftalmológica

## Configuración de Insomnia

1. Abre Insomnia
2. Ve a Preferences -> Data -> Import/Export
3. Selecciona "Import Data" -> "From File"
4. Selecciona el archivo `insomnia/endpoints.json`

## Variables de Entorno

Configura las siguientes variables de entorno en Insomnia:

```json
{
  "base_url": "http://localhost:8000",
  "token": "tu-token-jwt-aquí"
}
```

## Endpoints Disponibles

### Autenticación
- POST /api/auth/login - Iniciar sesión

### Pacientes
- GET /api/pacientes - Obtener lista de pacientes
- POST /api/pacientes - Crear nuevo paciente
- GET /api/pacientes/{id} - Obtener paciente específico
- PUT /api/pacientes/{id} - Actualizar paciente
- DELETE /api/pacientes/{id} - Eliminar paciente

### Citas
- GET /api/citas - Obtener lista de citas
- POST /api/citas - Crear nueva cita
- GET /api/citas/{id} - Obtener cita específica
- PUT /api/citas/{id} - Actualizar cita
- DELETE /api/citas/{id} - Eliminar cita