Okay, analicemos la estructura de tu base de datos y el problema del 403 Forbidden.

Entendiendo la estructura para Superadministradores:

users:

id: Identificador del usuario.

role_id: Clave foránea a la tabla roles. Para un superadministrador, este role_id debería apuntar al ID del rol "SuperAdministrador".

associated_clinic_id: Para un superadministrador, este campo idealmente debería ser NULL, ya que no están restringidos a una clínica específica.

El usuario root que tienes (id=1) tiene role_id=1 y associated_clinic_id=NULL, lo cual es correcto para un SuperAdmin.

roles:

id=1, name='SuperAdministrador'. Esto es correcto.

permissions:

Tienes permisos bien definidos, como admin.gestionar_usuarios (id=1).

rolepermissions:

Aquí se vinculan los roles con los permisos.

Para role_id=1 (SuperAdministrador), tienes asignados los permisos:

permission_id=1 (admin.gestionar_usuarios)

permission_id=2 (admin.gestionar_roles)

permission_id=3 (admin.gestionar_clinicas)

permission_id=4 (paciente.ver_todos)

permission_id=9 (expediente.ver)

El problema del 403 Forbidden:

Un 403 Forbidden significa que el usuario está autenticado (el sistema sabe quién es), pero no tiene los permisos necesarios para acceder al recurso solicitado (/api/v1/users/).

Dado que tu usuario root tiene el rol SuperAdministrador y este rol tiene el permiso admin.gestionar_usuarios, la configuración de la base de datos parece correcta. El problema probablemente reside en la lógica de tu aplicación (FastAPI/Python):

Posibles causas y cómo solucionarlo en tu aplicación (FastAPI):

Nombre del Permiso Incorrecto en el Código:

Problema: En tu código FastAPI, al proteger el endpoint /api/v1/users/, podrías estar verificando un nombre de permiso diferente al que tienes en la base de datos (ej. manage_users en lugar de admin.gestionar_usuarios).

Solución: Asegúrate de que el string del permiso que usas en tu decorador o dependencia de autorización coincida exactamente con el name en la tabla permissions.

Lógica de Verificación de Permisos:

Problema: La función que verifica los permisos del usuario podría tener un error. Por ejemplo, podría estar buscando el permiso en el lugar incorrecto o la comparación podría ser defectuosa.

Solución: Revisa cómo cargas los permisos del usuario actual y cómo los comparas con el permiso requerido para el endpoint.

# Ejemplo conceptual de una dependencia de autorización en FastAPI
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
# Asume que tienes modelos SQLAlchemy: User, Role, Permission, RolePermission
# Asume que tienes una función get_current_user que devuelve el usuario autenticado

def get_db(): # Tu dependencia para obtener la sesión de BD
    # ...
    pass

def user_has_permission(db: Session, user_id: int, permission_name: str) -> bool:
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.role:
        return False

    # Opción 1: Cargar directamente los permisos del rol
    # Esto asume que tienes una relación `permissions` en tu modelo Role
    # que se carga a través de la tabla `rolepermissions`
    # Ejemplo: role = db.query(Role).options(joinedload(Role.permissions)).filter(Role.id == user.role_id).first()
    # for perm in role.permissions:
    # if perm.name == permission_name:
    # return True

    # Opción 2: Consulta explícita a través de rolepermissions
    permission_record = db.query(Permission).filter(Permission.name == permission_name).first()
    if not permission_record:
        return False # El permiso no existe en la DB

    role_permission = db.query(RolePermission).filter(
        RolePermission.role_id == user.role_id,
        RolePermission.permission_id == permission_record.id
    ).first()
    return role_permission is not None


def require_permission(permission_name: str):
    async def _require_permission(
        current_user: User = Depends(get_current_active_user), # Tu función de autenticación
        db: Session = Depends(get_db)
    ):
        if not user_has_permission(db, current_user.id, permission_name):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user # Devuelve el usuario si tiene permiso
    return _require_permission

# En tu router:
# from .dependencies import require_permission (o donde lo definas)

@router.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    # Aquí aplicas la dependencia
    current_user: models.User = Depends(require_permission("admin.gestionar_usuarios"))
):
    users = crud.get_users(db, skip=skip, limit=limit) # Tu función CRUD
    return users


Filtro por associated_clinic_id Inapropiado para SuperAdmin:

Problema: Si tu lógica para obtener usuarios (o cualquier otro recurso) siempre filtra por current_user.associated_clinic_id sin considerar el rol, un SuperAdmin (con associated_clinic_id=NULL) no verá nada o podría causar un error que se traduce en un 403.

Solución: Tu capa de servicio o CRUD debe tener una lógica para omitir el filtro de clínica si el usuario es SuperAdministrador.

# En tu archivo crud.py (o donde tengas la lógica de acceso a datos)
def get_users(db: Session, current_user: models.User, skip: int = 0, limit: int = 100):
    query = db.query(models.User)

    # IMPORTANTE: Solo filtrar por clínica si NO es SuperAdmin
    # Asumiendo que tienes acceso al nombre del rol del current_user
    # (por ejemplo, current_user.role.name)
    if current_user.role.name != "SuperAdministrador" and current_user.associated_clinic_id is not None:
        # Si es otro rol, puede que quieras filtrar usuarios de su misma clínica
        query = query.filter(models.User.associated_clinic_id == current_user.associated_clinic_id)
    # Para SuperAdmin, no se aplica filtro de clínica, puede ver todos.

    return query.offset(skip).limit(limit).all()

# Y en tu endpoint:
@router.get("/users/", response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_permission("admin.gestionar_usuarios"))
):
    # Pasas current_user a la función CRUD para que pueda decidir sobre el filtrado
    users = crud.get_users(db, current_user=current_user, skip=skip, limit=limit)
    return users
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Token JWT no actualizado o no incluye información de rol/permisos:

Problema: Si usas JWT, el token podría haber sido generado antes de que se asignaran los roles/permisos correctos, o el payload del token no incluye la información necesaria (como role_id o una lista de permisos) que tu sistema usa para la autorización.

Solución: Asegúrate de que al generar el token JWT, incluyas el role_id (o incluso los nombres de los permisos, aunque es menos común y puede hacer el token grande). Al validar el token y obtener el current_user, carga su rol y permisos desde la base de datos. Si cambias roles/permisos, el usuario podría necesitar desloguearse y loguearse de nuevo para obtener un token actualizado.

Cómo crear usuarios Superadministrativos:

Directamente en la Base de Datos (para el primer SuperAdmin):

Esto es lo que ya hiciste para el usuario root. Es la forma más sencilla de arrancar el sistema con un administrador inicial.

Simplemente inserta un registro en la tabla users con:

username, password_hash, email, first_name, last_name (los que quieras).

role_id: el id del rol 'SuperAdministrador' (en tu caso, 1).

associated_clinic_id: NULL.

is_active: 1.

A través de un Endpoint Protegido (para SuperAdmins subsiguientes):

Crea un endpoint (ej. POST /api/v1/users/ o POST /api/v1/admin/users/) que permita crear usuarios.

Protege este endpoint para que solo un SuperAdministrador existente (que tenga el permiso admin.gestionar_usuarios) pueda acceder a él.

En el payload de este endpoint, podrías permitir especificar el role_id para el nuevo usuario.

# En tu router de usuarios o un router de administración
@router.post("/users/", response_model=schemas.User, status_code=status.HTTP_201_CREATED)
def create_new_user(
    user_in: schemas.UserCreate, # Tu Pydantic model para crear usuarios
    db: Session = Depends(get_db),
    # Solo SuperAdmins con permiso pueden crear otros usuarios
    # (podrías tener un permiso más específico si quieres, ej: "admin.crear_superadmin")
    current_admin: models.User = Depends(require_permission("admin.gestionar_usuarios"))
):
    # En user_in.role_id vendría el ID del rol para el nuevo usuario
    # Valida que el rol_id exista, etc.
    # Asegúrate de hashear la contraseña de user_in.password
    db_user = crud.create_user(db=db, user=user_in) # Tu función CRUD para crear
    return db_user
IGNORE_WHEN_COPYING_START
content_copy
download
Use code with caution.
Python
IGNORE_WHEN_COPYING_END

Pasos para depurar tu problema del 403:

Verifica el nombre del permiso: Confirma que en tu dependencia require_permission("...") estás usando "admin.gestionar_usuarios".

Depura la función user_has_permission: Coloca print() o usa un depurador para ver qué valores tienen user_id, user.role_id, permission_name, permission_record.id dentro de esta función cuando el usuario root intenta acceder al endpoint. Esto te dirá si está encontrando el rol y el permiso correctamente.

Verifica la lógica de get_current_active_user: Asegúrate de que está cargando correctamente el role_id y la información asociada al rol del usuario autenticado.

Revisa la consola de FastAPI: A veces, si hay un error no manejado dentro de una dependencia antes de que se lance el HTTPException explícito, FastAPI podría devolver un 500 o un 403 genérico. Busca cualquier traceback en la consola.

La estructura de tu base de datos es sólida para manejar esto. El problema casi con seguridad está en cómo tu código FastAPI interpreta y usa esta estructura para la autorización.