"""
Ponto de entrada do AFSESAB Middleware Logístico.

Este módulo inicializa a interface gráfica principal, o cliente HTTPX para
a API e gerencia o roteamento de componentes visuais baseados na escolha do menu.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from sqlalchemy.orm import Session

# --- Importação dos Nossos Módulos ---
from database import SessionLocal, init_db
from models import UnidadeLocal
from api_client import ClienteAFSESAB

# --- Importação das Nossas Telas Componentizadas ---
from Telas.tela_estoque import TelaEstoque
from Telas.tela_pacientes import TelaPacientes


class AppLogistica(ttk.Window):
    """
    Janela Principal e Controlador de Rotas da aplicação.
    """

    def __init__(self, api_client):
        super().__init__(themename="superhero")
        self.api_client = api_client
        self.title("AFSESAB - Logística Integrada")
        self.attributes("-fullscreen", True)

        self.frame_atual = None
        self.area_conteudo = None
        self.unidade_ativa = None

        self.construir_tela_login()

    def limpar_tela_inteira(self):
        if self.frame_atual:
            self.frame_atual.destroy()

    def limpar_area_conteudo(self):
        """ Destrói os widgets antigos do painel direito antes de injetar a nova tela. """
        if self.area_conteudo:
            for widget in self.area_conteudo.winfo_children():
                widget.destroy()

    # ==========================================
    # FLUXO DE LOGIN (Mantido)
    # ==========================================
    def construir_tela_login(self):
        self.limpar_tela_inteira()
        self.frame_atual = ttk.Frame(self, padding=40)
        self.frame_atual.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.frame_atual, text="Acesso Logístico",
                  font=("Helvetica", 24, "bold")).pack(pady=(0, 30))

        ttk.Label(self.frame_atual, text="E-mail / Usuário:").pack(anchor="w")
        self.entry_usuario = ttk.Entry(self.frame_atual, width=40)
        self.entry_usuario.pack(pady=5)

        ttk.Label(self.frame_atual, text="Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(self.frame_atual, width=40, show="*")
        self.entry_senha.pack(pady=5)

        ttk.Button(self.frame_atual, text="Entrar", bootstyle=PRIMARY,
                   command=self.acao_login).pack(pady=20)
        ttk.Button(self.frame_atual, text="Sair do Sistema",
                   bootstyle=DANGER, command=self.destroy).pack(pady=5)

    def acao_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning(
                "Atenção", "Preencha o e-mail/usuário e a senha.")
            return

        sucesso_api = self.api_client.autenticar(usuario, senha)

        if sucesso_api:
            self.construir_tela_selecao_unidade()
        else:
            messagebox.showerror("Erro de Autenticação",
                                 "Credenciais inválidas.")

    # ==========================================
    # SELEÇÃO DE UNIDADE (Mantida)
    # ==========================================
    def construir_tela_selecao_unidade(self):
        self.limpar_tela_inteira()
        self.frame_atual = ttk.Frame(self, padding=40)
        self.frame_atual.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.frame_atual, text="Selecione sua Unidade",
                  font=("Helvetica", 18, "bold")).pack(pady=(0, 20))

        db: Session = SessionLocal()
        unidades_db = db.query(UnidadeLocal).all()
        db.close()

        self.mapa_unidades = {
            f"{u.cnes} - {u.nome_da_unidade}": u for u in unidades_db}
        nomes_para_combo = list(self.mapa_unidades.keys())

        if not nomes_para_combo:
            messagebox.showerror(
                "Erro no Banco", "Nenhuma unidade cadastrada no banco local.")
            self.construir_tela_login()
            return

        self.combo_unidade = ttk.Combobox(
            self.frame_atual, values=nomes_para_combo, width=50, state="readonly")
        self.combo_unidade.pack(pady=10)
        self.combo_unidade.current(0)

        ttk.Button(self.frame_atual, text="Confirmar Acesso",
                   bootstyle=SUCCESS, command=self.confirmar_unidade).pack(pady=20)

    def confirmar_unidade(self):
        selecao = self.combo_unidade.get()
        self.unidade_ativa = self.mapa_unidades[selecao]
        self.construir_tela_principal()

    # ==========================================
    # DASHBOARD & ROTEADOR REFEITO
    # ==========================================
    def construir_tela_principal(self):
        self.limpar_tela_inteira()
        self.frame_atual = ttk.Frame(self)
        self.frame_atual.pack(expand=True, fill=BOTH)
        self.frame_atual.columnconfigure(1, weight=1)
        self.frame_atual.rowconfigure(0, weight=1)

        sidebar = ttk.Frame(self.frame_atual, bootstyle=SECONDARY, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ttk.Label(sidebar, text="AFSESAB", font=("Helvetica", 20, "bold"),
                  bootstyle="inverse-secondary").pack(pady=(30, 5), padx=20)

        opcoes = ["Painel Inicial", "Meu Estoque",
                  "Lista de Pacientes", "Receber Pedidos"]
        for opt in opcoes:
            ttk.Button(sidebar, text=opt, bootstyle=(SUCCESS, OUTLINE),
                       command=lambda o=opt: self.renderizar_conteudo(o)).pack(fill=X, padx=20, pady=5)

        ttk.Button(sidebar, text="Sair / Trocar", bootstyle=DANGER,
                   command=self.construir_tela_login).pack(side=BOTTOM, pady=20, padx=20, fill=X)

        area_direita = ttk.Frame(self.frame_atual)
        area_direita.grid(row=0, column=1, sticky="nsew")

        header_frame = ttk.Frame(area_direita, padding=10, bootstyle="dark")
        header_frame.pack(side=TOP, fill=X)

        ttk.Label(header_frame, text=f"CNES: {self.unidade_ativa.cnes} | {self.unidade_ativa.nome_da_unidade}", font=(
            "Helvetica", 10, "bold"), bootstyle="inverse-dark").pack(side=RIGHT, padx=20)

        self.area_conteudo = ttk.Frame(area_direita, padding=30)
        self.area_conteudo.pack(expand=True, fill=BOTH)

        self.renderizar_conteudo("Painel Inicial")

    def renderizar_conteudo(self, modulo: str):
        """ 
        O Roteador: Apaga a tela atual e Injeta a Classe da tela solicitada.
        """
        self.limpar_area_conteudo()

        if modulo == "Painel Inicial":
            ttk.Label(self.area_conteudo, text="Painel Inicial", font=(
                "Helvetica", 24, "bold")).pack(anchor="w", pady=(0, 20))
            ttk.Label(self.area_conteudo,
                      text=f"Bem-vindo ao sistema da unidade {self.unidade_ativa.nome_da_unidade}.").pack(anchor="w")

        elif modulo == "Lista de Pacientes":
            # Injeta o componente TelaPacientes apontando para self.area_conteudo como pai
            TelaPacientes(master=self.area_conteudo,
                          cnes_ativa=self.unidade_ativa.cnes)

        elif modulo == "Meu Estoque":
            # Injeta o componente TelaEstoque apontando para self.area_conteudo como pai
            TelaEstoque(master=self.area_conteudo, api_client=self.api_client,
                        cnes_ativa=self.unidade_ativa.cnes)

        else:
            ttk.Label(self.area_conteudo, text=modulo, font=(
                "Helvetica", 24, "bold")).pack(anchor="w", pady=(0, 20))
            ttk.Label(self.area_conteudo,
                      text="Módulo em desenvolvimento...").pack(anchor="w")


if __name__ == "__main__":
    init_db()
    cliente_api = ClienteAFSESAB()
    app = AppLogistica(api_client=cliente_api)
    app.mainloop()
