from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Configuração da URL de Conexão Localhost
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:root@localhost:5432/postgres"

# 2. Configuração da Engine do SQLAlchemy
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

# 3. Base Declarativa para as Tabelas
Base = declarative_base()

# ==========================================
# FUNÇÃO DE INICIALIZAÇÃO ("START")
# ==========================================


def init_db():
    """
    Função de "start". Conecta ao banco de dados e cria todas as tabelas 
    e colunas mapeadas que ainda não existam no esquema.
    Não altera ou apaga dados de tabelas que já existem.
    """
    print("Verificando e inicializando banco de dados local...")
    Base.metadata.create_all(bind=engine)
    print("Banco de dados pronto para uso.")


if __name__ == "__main__":
    init_db()
