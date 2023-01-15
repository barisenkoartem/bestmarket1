from aiogram.dispatcher.fsm.state import State, StatesGroup

class AdminState(StatesGroup):
    STATUS = State()
    LIST = State()
    MAILING = State()
    MSG = State()

class ReplenishState(StatesGroup):
    AMOUNT = State()
    PAYMENT_METHOD = State()
    CHECK_BILL = State()
    CHECK = State()
    CANCEL = State()
    
    
class GoldState(StatesGroup):
    GOLD_RUB = State()
    RUB_GOLD = State()
    
    REPLENISH_AMOUNT = State()
    REPLENISH_CONFIRM = State()
    
    OUTPUT_AMOUNT = State()
    OUTPUT_ITEM = State()
    
    REVIEWS = State()
    CANCEL = State()
    
    
class PromoCodeState(StatesGroup):
    TITLE = State()

    
class SupportState(StatesGroup):
    QUESTION = State()
    REPLY = State()
    

class CubeState(StatesGroup):
    amount = State()
    

class BowlingState(StatesGroup):
    amount = State()
    
class BasketballState(StatesGroup):
    amount = State()
    
    
class ProductState(StatesGroup):
    price_type = State()
    name = State()
    price = State()
    description = State()
    photo = State()