"""
Módulo de configuração e infraestrutura do Banco de Dados.

Gerencia a engine de conexão com o PostgreSQL, o pool de conexões 
e a fábrica de sessões (SessionLocal).
"""

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from models import Base, UnidadeLocal, Atendimento, LogImportacao, Paciente


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/postgres"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    client_encoding='utf8',
    echo=True,           # Mude para True se quiser ver o SQL gerado no terminal
    pool_pre_ping=True,   # Verifica se a conexão caiu antes de usá-la
    pool_recycle=300,
    pool_size=5,
    max_overflow=10
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Função de "start". Conecta ao banco de dados e cria todas as tabelas 
    e colunas mapeadas que ainda não existam no esquema.
    Não altera ou apaga dados de tabelas que já existem.
    """
    print("Verificando e inicializando banco de dados local...")

    # O comando create_all lê o metadata da Base e gera os comandos CREATE TABLE
    Base.metadata.create_all(bind=engine)

    print("Banco de dados pronto para uso.")
