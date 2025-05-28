from .auth import auth_router
from .users import users_router

# Exportar los routers para que main.py pueda importarlos fácilmente
__all__ = ["auth_router", "users_router"]