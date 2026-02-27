import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
# Importe a classe ClienteAFSESAB que criamos anteriormente
# from sua_api import ClienteAFSESAB


class AppLogistica(ttk.Window):
    def __init__(self, api_client):
        super().__init__(themename="superhero")
        self.api_client = api_client
        self.title("AFSESAB - Logística Integrada")
        self.attributes("-fullscreen", True)
        self.frame_atual = None

        # Variável de estado para armazenar a unidade escolhida após o login
        self.unidade_ativa = None

        # Garante que temos algumas unidades no banco para teste (opcional)
        self._popular_banco_se_vazio()

        self.construir_tela_login()

    def _popular_banco_se_vazio(self):
        """ Função de apoio: insere dados de teste se o banco Neon estiver vazio """
        db = SessionLocal()
        if db.query(UnidadeLocal).count() == 0:
            db.add_all([
                UnidadeLocal(cnes="1234567",
                             nome_da_unidade="HGE - Hospital Geral do Estado"),
                UnidadeLocal(cnes="7654321",
                             nome_da_unidade="Hospital Roberto Santos")
            ])
            db.commit()
        db.close()

    def limpar_tela(self):
        if self.frame_atual:
            self.frame_atual.destroy()

    def construir_tela_login(self):
        self.limpar_tela()
        self.frame_atual = ttk.Frame(self, padding=40)
        self.frame_atual.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.frame_atual, text="Acesso Logístico",
                  font=("Helvetica", 24, "bold")).pack(pady=(0, 30))

        ttk.Label(self.frame_atual, text="E-mail:").pack(anchor="w")
        self.entry_email = ttk.Entry(self.frame_atual, width=40)
        self.entry_email.pack(pady=5)

        ttk.Label(self.frame_atual, text="Senha:").pack(anchor="w")
        self.entry_senha = ttk.Entry(self.frame_atual, width=40, show="*")
        self.entry_senha.pack(pady=5)

        ttk.Button(self.frame_atual, text="Entrar", bootstyle=PRIMARY,
                   command=self.acao_login).pack(pady=20)
        ttk.Button(self.frame_atual, text="Sair", bootstyle=DANGER,
                   command=self.destroy).pack(pady=5)

    def acao_login(self):
        email = self.entry_email.get()
        senha = self.entry_senha.get()

        if not email or not senha:
            messagebox.showwarning("Atenção", "Preencha todos os campos.")
            return

        # self.api_client.autenticar(email, senha) <- Descomente em produção
        sucesso_api = True  # Mock para testarmos a UI

        if sucesso_api:
            # Login via API ocorreu! Agora vamos pedir para ele dizer em qual unidade está
            self.construir_tela_selecao_unidade()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def construir_tela_selecao_unidade(self):
        """ Nova tela intermediária consultando nosso PostgreSQL """
        self.limpar_tela()
        self.frame_atual = ttk.Frame(self, padding=40)
        self.frame_atual.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.frame_atual, text="Selecione sua Unidade de Operação", font=(
            "Helvetica", 18, "bold")).pack(pady=(0, 20))

        # 1. Faz o GET (Query) no PostgreSQL Neon
        db = SessionLocal()
        unidades_db = db.query(UnidadeLocal).all()
        db.close()

        # 2. Formata para o Combobox
        self.mapa_unidades = {
            f"{u.cnes} - {u.nome_da_unidade}": u for u in unidades_db}
        nomes_para_combo = list(self.mapa_unidades.keys())

        # 3. Widget de Combobox do ttkbootstrap
        self.combo_unidade = ttk.Combobox(
            self.frame_atual, values=nomes_para_combo, width=50, state="readonly")
        self.combo_unidade.pack(pady=10)
        if nomes_para_combo:
            self.combo_unidade.current(0)  # Seleciona o primeiro por padrão

        ttk.Button(self.frame_atual, text="Confirmar Unidade e Acessar",
                   bootstyle=SUCCESS, command=self.confirmar_unidade).pack(pady=20)

    def confirmar_unidade(self):
        selecao = self.combo_unidade.get()
        if not selecao:
            messagebox.showwarning(
                "Atenção", "Selecione uma unidade para continuar.")
            return

        # Salva o objeto Unidade (id, cnes, nome_da_unidade) na sessão da nossa aplicação
        self.unidade_ativa = self.mapa_unidades[selecao]

        # Pula para o Dashboard principal
        self.construir_tela_principal()

    def construir_tela_principal(self):
        self.limpar_tela()
        self.frame_atual = ttk.Frame(self)
        self.frame_atual.pack(expand=True, fill=BOTH)

        self.frame_atual.columnconfigure(1, weight=1)
        self.frame_atual.rowconfigure(0, weight=1)

        # ====== SIDEBAR ======
        sidebar = ttk.Frame(self.frame_atual, bootstyle=SECONDARY, width=250)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ttk.Label(sidebar, text="AFSESAB\nLogística", font=(
            "Helvetica", 18, "bold"), bootstyle="inverse-secondary").pack(pady=30, padx=20)

        opcoes = ["Painel Inicial", "Receber Pedidos", "Dispensação"]
        for opt in opcoes:
            ttk.Button(sidebar, text=opt, bootstyle=(
                SUCCESS, OUTLINE)).pack(fill=X, padx=20, pady=5)

        ttk.Button(sidebar, text="Sair", bootstyle=DANGER, command=self.construir_tela_login).pack(
            side=BOTTOM, pady=20, padx=20, fill=X)

        # ====== ÁREA DE CONTEÚDO (DIREITA) ======
        area_direita = ttk.Frame(self.frame_atual)
        area_direita.grid(row=0, column=1, sticky="nsew")

        # HEADER SUPERIOR (Aqui ficará o CNES da unidade)
        # O packer 'X' garante que ele ocupe toda a largura horizontal da tela [5]
        header_frame = ttk.Frame(area_direita, padding=10, bootstyle="dark")
        header_frame.pack(side=TOP, fill=X)

        # Formatando CNES - Nome e forçando para a direita (side=RIGHT) [5]
        texto_unidade = f"Unidade Ativa: {self.unidade_ativa.cnes} - {self.unidade_ativa.nome_da_unidade}"
        lbl_unidade = ttk.Label(header_frame, text=texto_unidade, font=(
            "Helvetica", 10, "bold"), bootstyle="inverse-dark")
        lbl_unidade.pack(side=RIGHT, padx=20)

        # Container Principal para as trocas de tela
        self.area_conteudo = ttk.Frame(area_direita, padding=30)
        self.area_conteudo.pack(expand=True, fill=BOTH)

        self.lbl_titulo = ttk.Label(
            self.area_conteudo, text="Painel Inicial", font=("Helvetica", 24))
        self.lbl_titulo.pack(anchor="w")


if __name__ == "__main__":
    app = AppLogistica(api_client=None)
    app.mainloop()

Decisões de Arquitetura tomadas aqui:

    Segregação do Banco(Engine e Session): Usamos a factory sessionmaker do SQLAlchemy ligada à sua URL remota. O session manager garante que abrimos e fechamos conexões com o pool da Neon Cloud da forma mais eficiente, evitando vazamento de memória.
    Uso de Combobox(ttkbootstrap): Quando puxamos do banco a lista com o comando SQLAlchemy db.query(UnidadeLocal).all(), montamos um dicionário(self.mapa_unidades). Isso nos permite exibir apenas a string limpa para o usuário na interface visual e, assim que ele clica em "Confirmar", resgatamos o objeto UnidadeLocal com ID, CNES e Nome limpos, gravando na variável global self.unidade_ativa.
    Canto Superior Direito: Criei um header_frame no topo da área_direita. Usando os comandos da geometria do packer do tkinter(pack(side=RIGHT) e fill=X), a barra preta escura do header ocupará toda a tela de ponta a ponta e a string "CNES - Nome" nascerá sempre perfeitamente alinhada na âncora à extrema direita.

O código está isolado e seguro para uso. Execute, faça o "mock" de login e teste a integração PostgreSQL! O que achou do novo fluxo?
Como implementar um sistema de busca dinâmica para as unidades?
Qual o melhor modo para gerenciar sesses de usurio?
Como proteger as credenciais de banco no código fonte?

File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\engine\base.py", line 143, in init
self._dbapi_connection = engine.raw_connection()
~~~~~~~~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\engine\base.py", line 3309, in raw_connection
return self.pool.connect()
~~~~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 447, in connect
return _ConnectionFairy._checkout(self)
~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 1264, in _checkout
fairy = _ConnectionRecord.checkout(pool)
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 711, in checkout
rec = pool._do_get()
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\impl.py", line 177, in _do_get
with util.safe_reraise():
~~~~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\util\langhelpers.py", line 224, in exit
raise exc_value.with_traceback(exc_tb)
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\impl.py", line 175, in _do_get
return self._create_connection()
~~~~~~~~~~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 388, in _create_connection
return _ConnectionRecord(self)
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 673, in init
self.__connect()
~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 899, in __connect
with util.safe_reraise():
~~~~~~~~~~~~~~~~~^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\util\langhelpers.py", line 224, in exit
raise exc_value.with_traceback(exc_tb)
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\pool\base.py", line 895, in __connect
self.dbapi_connection = connection = pool.invoke_creator(self)
~~~~~~~~~~~~~~~~~~~~^^^^^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\engine\create.py", line 661, in connect
return dialect.connect(*cargs, **cparams)
~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\sqlalchemy\engine\default.py", line 630, in connect
return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
File "C:\Users\bernardo.silva\AppData\Roaming\Python\Python313\site-packages\psycopg2_init.py", line 135, in connect
conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: connection to server at "ep-royal-night-acckjdmd-pooler.sa-east-1.aws.neon.tech" (18.230.255.48), port 5432 failed: server closed the connection unexpectedly
This probably means the server terminated abnormally
before or while processing the request.
Addressing the Interruption...
