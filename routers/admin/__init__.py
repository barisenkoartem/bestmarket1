from . import admin_help, rubles, gold, user, promo, code, mailing, product

admin = (admin_help.router, rubles.router, gold.router, user.router, promo.router, code.router, mailing.router, product.router)