from .users import users_routers
from .commands import commands_router

routers = (*users_routers, *commands_router)
