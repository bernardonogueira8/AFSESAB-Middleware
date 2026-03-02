import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from sqlalchemy.orm import Session

from database import SessionLocal, UnidadeLocal, paciente, Atendimento, init_db

# IMPORTANDO NOSSO NOVO CLIENTE DE API
from api_client import ClienteAFSESAB


class AppLogistica(ttk.Window):
    def __init__(self, api_client):  # <-- Garanta que __init__ recebe api_client
        super().__init__(themename="superhero")
        self.api_client = api_client  # <-- Salvando o cliente na classe
        self.title("AFSESAB - Logística Integrada")
        self.attributes("-fullscreen", True)

        # Gerenciamento de estado da UI
        self.frame_atual = None
        self.area_conteudo = None  # Referência fixa para a área da direita
        self.unidade_ativa = None

        self.construir_tela_login()

    def limpar_tela_inteira(self):
        """ Destrói a janela inteira (usado nas trocas Login -> Seleção -> Main) """
        if self.frame_atual:
            self.frame_atual.destroy()

    def limpar_area_conteudo(self):
        """ Destrói apenas os componentes da tela ativa no painel direito """
        if self.area_conteudo:
            for widget in self.area_conteudo.winfo_children():
                widget.destroy()

    # ==========================================
    # FLUXO DE LOGIN E UNIDADE
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
        # 1. Captura os dados digitados pelo usuário no formulário
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        # 2. Validação local básica de preenchimento
        if not usuario or not senha:
            messagebox.showwarning(
                "Atenção", "Preencha o e-mail/usuário e a senha.")
            return

        # 3. Chama a nossa camada de API (Isso vai popular a variável self.api_client.token)
        sucesso_api = self.api_client.autenticar(usuario, senha)

        # 4. Bloqueia a entrada na interface se a API recusar o login
        if sucesso_api:
            # Login ocorreu com sucesso e o Token JWT está em memória!
            # Avançamos para a tela do Banco de Dados local.
            self.construir_tela_selecao_unidade()
        else:
            # A API retornou False (Credencial inválida ou o servidor do AFSESAB está fora do ar)
            messagebox.showerror(
                "Erro de Autenticação", "Credenciais inválidas ou erro de rede. Verifique seu acesso.")

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
                "Erro no Banco", "Nenhuma unidade cadastrada no banco de dados local.")
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
    # DASHBOARD PRINCIPAL & ROTEAMENTO
    # ==========================================
    def construir_tela_principal(self):
        self.limpar_tela_inteira()
        self.frame_atual = ttk.Frame(self)
        self.frame_atual.pack(expand=True, fill=BOTH)
        self.frame_atual.columnconfigure(1, weight=1)
        self.frame_atual.rowconfigure(0, weight=1)

        # 1. SIDEBAR VERTICAL
        sidebar = ttk.Frame(self.frame_atual, bootstyle=SECONDARY, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ttk.Label(sidebar, text="AFSESAB", font=("Helvetica", 20, "bold"),
                  bootstyle="inverse-secondary").pack(pady=(30, 5), padx=20)
        ttk.Label(sidebar, text="Módulo Logístico", font=("Helvetica", 10),
                  bootstyle="inverse-secondary").pack(pady=(0, 20), padx=20)

        # Lista de Módulos (Roteamento)
        opcoes = [
            "Painel Inicial", "Receber Pedidos", "Dispensação",
            "Meu Estoque", "Lista de Pacientes", "Lista de Medicamentos",
            "Transferência de Estoque"
        ]

        for opt in opcoes:
            # O 'lambda' garante que cada botão passe seu nome para a função de roteamento
            ttk.Button(sidebar, text=opt, bootstyle=(SUCCESS, OUTLINE),
                       command=lambda o=opt: self.renderizar_conteudo(o)).pack(fill=X, padx=20, pady=5)

        ttk.Button(sidebar, text="Sair / Trocar Unidade", bootstyle=DANGER,
                   command=self.construir_tela_login).pack(side=BOTTOM, pady=20, padx=20, fill=X)

        # 2. ÁREA DA DIREITA (HEADER + CONTEÚDO)
        area_direita = ttk.Frame(self.frame_atual)
        area_direita.grid(row=0, column=1, sticky="nsew")

        header_frame = ttk.Frame(area_direita, padding=10, bootstyle="dark")
        header_frame.pack(side=TOP, fill=X)

        texto_unidade = f"CNES: {self.unidade_ativa.cnes} | {self.unidade_ativa.nome_da_unidade}"
        ttk.Label(header_frame, text=texto_unidade, font=(
            "Helvetica", 10, "bold"), bootstyle="inverse-dark").pack(side=RIGHT, padx=20)

        # Esta é a área que será limpada e reescrita a cada clique no menu
        self.area_conteudo = ttk.Frame(area_direita, padding=30)
        self.area_conteudo.pack(expand=True, fill=BOTH)

        # Inicia a tela padrão
        self.renderizar_conteudo("Painel Inicial")

    def renderizar_conteudo(self, modulo: str):
        self.limpar_area_conteudo()

        ttk.Label(self.area_conteudo, text=modulo, font=(
            "Helvetica", 24, "bold")).pack(anchor="w", pady=(0, 20))

        if modulo == "Painel Inicial":
            ttk.Label(self.area_conteudo,
                      text=f"Bem-vindo ao sistema da unidade {self.unidade_ativa.nome_da_unidade}.").pack(anchor="w")

        elif modulo == "Lista de Pacientes":
            self.tela_lista_pacientes()

        elif modulo == "Meu Estoque":
            self.tela_meu_estoque()  # <--- Adicionamos o roteamento aqui

        elif modulo == "Receber Pedidos":
            ttk.Label(self.area_conteudo, text="Aguardando leitura de QR Code do pacote...").pack(
                anchor="w")

        else:
            ttk.Label(self.area_conteudo,
                      text="Módulo em desenvolvimento...").pack(anchor="w")

    # ==========================================
    # SUB-TELAS DE CONTEÚDO
    # ==========================================
    def tela_meu_estoque(self):
        """ 
        Consulta a API de estoque, filtra o JSON pelo slugprogramasaude e renderiza na tela 
        """
        # Criando um Frame para os botões de ação acima da tabela
        frame_acoes = ttk.Frame(self.area_conteudo)
        # O packer é usado para controlar onde os widgets aparecem [2, 3]
        frame_acoes.pack(fill=X, pady=(0, 10))

        ttk.Label(frame_acoes, text="Filtro Ativo: Ação Judicial",
                  bootstyle="info").pack(side=LEFT)
        ttk.Button(frame_acoes, text="Atualizar Estoque", bootstyle=(SUCCESS, OUTLINE),
                   command=lambda: self.renderizar_conteudo("Meu Estoque")).pack(side=RIGHT)

        # Configuração da Tabela (Treeview)
        colunas = ("simpas",  "medicamento",  "lote",
                   "validade", "quantidade")
        tabela = ttk.Treeview(
            self.area_conteudo, columns=colunas, show="headings", bootstyle=PRIMARY)

        tabela.heading("simpas", text="Cód. SIMPAS")
        tabela.heading("medicamento", text="Medicamento")
        tabela.heading("lote", text="Lote")
        tabela.heading("validade", text="Data de Venc.")
        tabela.heading("quantidade", text="Qtd. em Estoque.")

        tabela.column("simpas", width=150, anchor="center")
        tabela.column("medicamento", width=400)
        tabela.column("lote", width=100, anchor="center")
        tabela.column("validade", width=120, anchor="center")
        tabela.column("quantidade", width=100, anchor="center")

        # 1. Fazendo a chamada na API
        resposta_api = self.api_client.consultar_estoque_unidade(
            self.unidade_ativa.cnes)

        # 2. Processando e Filtrando os Dados
        if resposta_api.get("success"):
            dados_estoque = resposta_api.get("data", [])

            # Filtro Pythonic usando List Comprehension (muito rápido e limpo em memória)
            estoque_acao_judicial = [
                item for item in dados_estoque
                if item.get("slugprogramasaude") == "acaoJudicial"
            ]

            # 3. Populando a tabela com os dados filtrados
            for item in estoque_acao_judicial:
                # Tratamento básico da string de data para tirar os '00:00:00'
                data_vencimento = item.get("datavencimento", "")[:10]

                tabela.insert("", END, values=(
                    item.get("codigosimpas"),
                    item.get("nomemedicamento"),
                    item.get("lote"),
                    data_vencimento,
                    item.get("quantidadeestoque")
                ))

            if not estoque_acao_judicial:
                messagebox.showinfo(
                    "Estoque", "Nenhum medicamento de Ação Judicial encontrado no estoque desta unidade.")

        else:
            messagebox.showerror(
                "Erro de Comunicação", "Não foi possível carregar o estoque via API do AFSESAB.")

        # O pack() fará a tabela expandir preenchendo o espaço disponível na tela [2, 3]
        tabela.pack(expand=True, fill=BOTH)

    def tela_lista_pacientes(self):
        """ Consulta o banco de dados via SQLAlchemy e exibe numa Tabela (Treeview) """

        # 1. Faz o GET (Select) no Banco de Dados
        db: Session = SessionLocal()
        # Filtramos para buscar apenas pacientes da unidade atualmente logada (usando o cnes) [4]
        pacientes_db = db.query(paciente).filter_by(
            cnes_dispensadora=self.unidade_ativa.cnes).all()
        db.close()

        # 2. Cria a Tabela (Treeview) para exibir os dados
        colunas = ("id", "nome", "cpf")
        tabela = ttk.Treeview(
            self.area_conteudo, columns=colunas, show="headings", bootstyle=PRIMARY)

        # Configura os cabeçalhos
        tabela.heading("id", text="ID")
        tabela.heading("nome", text="Nome do Paciente")
        tabela.heading("cpf", text="CPF")

        # Configura o tamanho das colunas
        tabela.column("id", width=50, anchor="center")
        tabela.column("nome", width=400)
        tabela.column("cpf", width=150, anchor="center")

        # Preenche a tabela com os dados do ORM
        for p in pacientes_db:
            tabela.insert("", END, values=(p.id, p.nome_do_paciente, p.cpf))

        tabela.pack(expand=True, fill=BOTH, pady=10)

        # Botão extra na tela para ações
        frame_botoes = ttk.Frame(self.area_conteudo)
        frame_botoes.pack(fill=X, pady=10)

        ttk.Button(frame_botoes, text="Atualizar Lista via API",
                   bootstyle=INFO).pack(side=LEFT)


if __name__ == "__main__":
    init_db()

    # 1. Instanciamos o nosso cliente de API que vai conversar com o AFSESAB
    cliente_api = ClienteAFSESAB()

    # 2. Injetamos o cliente de API dentro da nossa Interface Gráfica
    app = AppLogistica(api_client=cliente_api)
    app.mainloop()
