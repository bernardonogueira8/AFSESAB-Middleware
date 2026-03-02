"""
Módulo de mapeamento Objeto-Relacional (ORM).

Contém as definições de todas as tabelas do banco de dados PostgreSQL
utilizadas pelo middleware logístico, utilizando a Base Declarativa do SQLAlchemy 2.0.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class LogImportacao(Base):
    """
    Tabela de auditoria para importações de lotes e integrações via API.
    """
    __tablename__ = "log_importacao"
    id = Column(Integer, primary_key=True, index=True)
    data_hora = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    detalhes = Column(String(250), nullable=True)


class UnidadeLocal(Base):
    """
    Tabela de cache local das unidades de saúde.
    """
    __tablename__ = "unidades"
    id = Column(Integer, primary_key=True, index=True)
    cnes = Column(String(20), unique=True, index=True, nullable=False)
    nome_da_unidade = Column(String(150), nullable=False)


class Atendimento(Base):
    """
    Tabela de registros de dispensação e atendimento ao paciente.
    """
    __tablename__ = "atendimentos"
    id = Column(Integer, primary_key=True, index=True)
    cnes_dispensadora = Column(String(20), index=True, nullable=False)
    nome_do_paciente = Column(String(150), nullable=False)
    cpf = Column(String(20), index=True, nullable=False)
    n_sei = Column(String(50), nullable=False)
    qtd_autorizada = Column(Integer, nullable=False)
    cod_simpas = Column(String(20), nullable=False)
    lote_dispensado = Column(String(50), nullable=False)
    qtd_dispensada = Column(Integer, nullable=False)
    nome_lista_de_medicamentos = Column(String(250), nullable=False)
    frequencia_de_atendimento = Column(String(50), nullable=False)
    periodo_de_atendimento_meses = Column(String(20), nullable=False)
    periodo_de_tratamento = Column(String(50), nullable=False)
    data_do_atendimento = Column(String(20), nullable=False)
    data_do_retorno = Column(String(20), nullable=False)
    tipo_acao = Column(String(20), nullable=False)


class paciente(Base):
    """
    Tabela de cache de pacientes vinculados a uma unidade dispensadora.
    """
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    nome_do_paciente = Column(String(150), nullable=False)
    cpf = Column(String(20), index=True, nullable=False)
    cnes_dispensadora = Column(String(20), index=True, nullable=False)
