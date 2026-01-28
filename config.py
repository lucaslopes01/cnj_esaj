from decouple import config

class Config():
    MONGO_HOST=config('MONGO_HOST')
    MONGO_PORT=config('MONGO_PORT')
    MONGO_USR=config('MONGO_USR')
    MONGO_PWD=config('MONGO_PWD')
    MONGO_DB=config('MONGO_DB')
    MONGO_DB_ZOHO=config('MONGO_DB_ZOHO')
    AMBIENTE=config('AMBIENTE')
    TIME_BASIC=config('TIME_BASIC')
    TIME_TWO=config('TIME_TWO')
    TIME_TRHEE=config('TIME_TRHEE')
    TIME_MEDIUM=config('TIME_MEDIUM')
    TIME_LONG=config('TIME_LONG')
    DIARIO=config('DIARIO')
    RABBIT_HOST=config('RABBIT_HOST')
    RABBIT_PORT=config('RABBIT_PORT')
    RABBIT_USR=config('RABBIT_USR')
    RABBIT_PWD=config('RABBIT_PWD')
    TIME_PROCESS=config('TIME_PROCESS')

config = Config()