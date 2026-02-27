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
# DEFINIÇÃO DAS TABELAS (SCHEMAS)
# ==========================================


class UnidadeLocal(Base):
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    cnes = Column(String(20), unique=True, index=True, nullable=False)
    nome_da_unidade = Column(String(150), nullable=False)


class Atendimento(Base):
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True, index=True)
    cnes_dispensadora = Column(String(20), index=True, nullable=False)
    nome_do_paciente = Column(String(150), nullable=False)
    cpf = Column(String(20), index=True, nullable=False)
    n_sei = Column(String(50), nullable=False)
    cod_simpas = Column(String(20), nullable=False)
    qtd_autorizada = Column(Integer, nullable=False)
    nome_lista_de_medicamentos = Column(String(250), nullable=False)
    status_do_atendimento = Column(String(20), nullable=False)
    periodo_de_atendimento_meses = Column(String(20), nullable=False)
    frequencia_de_atendimento = Column(String(50), nullable=False)
    periodo_de_tratamento = Column(String(50), nullable=False)
    data_do_atendimento = Column(String(20), nullable=False)
    data_do_retorno = Column(String(20), nullable=False)
    tipo_acao = Column(String(20), nullable=False)


class LogImportacao(Base):
    __tablename__ = "log_importacao"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    detalhes = Column(String(250), nullable=True)


class paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome_do_paciente = Column(String(150), nullable=False)
    cpf = Column(String(20), index=True, nullable=False)
    cnes_dispensadora = Column(String(20), index=True, nullable=False)

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
