from . import games, cube, back_games, bowling, basketball

game = (games.router,
cube.router,
back_games.router,
bowling.router,
basketball.router)