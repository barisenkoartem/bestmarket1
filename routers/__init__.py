from .gold import gold
from .admin import admin
from .game import game
from . import (
    menu,
    start,
    profile,
    replenish,
    reviews,
    support,
    promo_code,
    not_command,
    case,
    product
)

main = (
    menu.router, 
    start.router, 
    profile.router, 
    replenish.router, 
    reviews.router, 
    support.router, 
    promo_code.router,
    case.router,
    product.router)

routers = [
    *main,
    *gold,
    *admin,
    *game,
    not_command.router
    ]