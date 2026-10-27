import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

class Conectar:
    def conectar():
        try:
            database_url = os.getenv("DATABASE_URL")
            if database_url:
                return psycopg.connect(database_url)

            conn = psycopg.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT", "5432")
            )
            return conn
        except Exception as erro:
            print(f"Erro de conexão com o PostgreSQL: {erro}")
            raise erro

