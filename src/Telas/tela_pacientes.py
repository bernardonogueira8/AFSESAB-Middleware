"""
Módulo visual da Lista de Pacientes.

Renderiza a tabela com os dados resgatados do banco de dados local (PostgreSQL),
filtrando os pacientes pertencentes à unidade atualmente logada.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from sqlalchemy.orm import Session

# Importa a conexão de banco de dados e o modelo diretamente
from database import SessionLocal
from models import Paciente


class TelaPacientes(ttk.Frame):
    """
    Componente de interface para listagem e gerenciamento de pacientes.

    Este componente instancia sua própria conexão com o banco de dados
    para buscar os registros de pacientes vinculados ao CNES ativo.

    Attributes:
        cnes_ativa (str): O CNES da unidade logada, usado para filtragem no ORM.
    """

    def __init__(self, master, cnes_ativa: str):
        """
        Inicializa o componente visual e anexa ao contêiner pai.

        Args:
            master (tk.Widget): O contêiner pai onde a tela será renderizada.
            cnes_ativa (str): Código CNES para isolamento de dados no banco.
        """
        super().__init__(master, padding=20)
        self.pack(expand=True, fill=BOTH)
        self.cnes_ativa = cnes_ativa

        self._construir_interface()

    def _construir_interface(self):
        """
        Monta a estrutura de tabela (Treeview), os cabeçalhos e preenche os dados.
        """
        # Header da Tela
        ttk.Label(self, text="Lista de Pacientes", font=(
            "Helvetica", 24, "bold")).pack(anchor="w", pady=(0, 20))

        # 1. Faz o GET (Select) no Banco de Dados
        db: Session = SessionLocal()
        pacientes_db = db.query(paciente).filter_by(
            cnes_dispensadora=self.cnes_ativa).all()
        db.close()

        # 2. Cria a Tabela (Treeview) para exibir os dados
        colunas = ("id", "nome", "cpf")
        tabela = ttk.Treeview(self, columns=colunas,
                              show="headings", bootstyle=PRIMARY)

        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome do Paciente")
        tabela.heading("cpf", text="CPF")

        tabela.column("id", width=50, anchor="center")
        tabela.column("nome", width=400)
        tabela.column("cpf", width=150, anchor="center")

        # 3. Preenche a tabela
        for p in pacientes_db:
            tabela.insert("", END, values=(p.id, p.nome_do_paciente, p.cpf))

        tabela.pack(expand=True, fill=BOTH, pady=10)

        # 4. Botões de Ação
        frame_botoes = ttk.Frame(self)
        frame_botoes.pack(fill=X, pady=10)

        ttk.Button(frame_botoes, text="Sincronizar Pacientes via API",
                   bootstyle=INFO).pack(side=LEFT)
