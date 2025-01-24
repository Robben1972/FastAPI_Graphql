from environs import Env

env = Env()
env.read_env()

DB_URL = env('DB_URL')