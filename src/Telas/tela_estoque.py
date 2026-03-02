"""
Módulo responsável pela renderização da interface de Meu Estoque.
Fornece componentes visuais para listar medicamentos da unidade logada.
"""
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


class TelaEstoque(ttk.Frame):
    """
    Renderiza a tabela (Treeview) com os medicamentos do estoque atual.

    Esta classe herda de `ttk.Frame` e isola toda a lógica visual, 
    buscando os dados via injeção de dependência do `ClienteAFSESAB`.

    Attributes:
        api_client: Instância do cliente HTTP para chamadas autenticadas.
        cnes_ativa: String contendo o CNES da unidade para filtro de dados.
    """

    def __init__(self, master, api_client, cnes_ativa: str):
        """
        Inicializa o componente de tela de estoque.

        Args:
            master (tk.Widget): O container pai onde este frame será desenhado.
            api_client (ClienteAFSESAB): Cliente para realizar requisições GET.
            cnes_ativa (str): O código da unidade logada no sistema.
        """
        # Inicializa o Frame do ttkbootstrap preenchendo o espaço do master
        super().__init__(master, padding=20)
        self.pack(expand=True, fill=BOTH)

        self.api_client = api_client
        self.cnes_ativa = cnes_ativa

        self._construir_interface()

    def _construir_interface(self):
        """
        Monta a tabela, as colunas e consome o JSON da API.

        Warning:
            Se o Token JWT estiver expirado, a API do AFSESAB retornará um array
            vazio e a tabela não será populada.
        """
        # Header da Tela
        ttk.Label(self, text="Meu Estoque", font=(
            "Helvetica", 24, "bold")).pack(anchor="w", pady=(0, 20))

        # Configuração da Tabela (Treeview)
        colunas = ("lote", "simpas", "medicamento", "quantidade")
        tabela = ttk.Treeview(self, columns=colunas,
                              show="headings", bootstyle=PRIMARY)

        tabela.heading("lote", text="Lote")
        tabela.heading("simpas", text="Cód. SIMPAS")
        tabela.heading("medicamento", text="Medicamento")
        tabela.heading("quantidade", text="Qtd. Disp.")

        tabela.column("lote", width=100, anchor="center")
        tabela.column("simpas", width=150, anchor="center")
        tabela.column("medicamento", width=400)
        tabela.column("quantidade", width=100, anchor="center")

        # Chama a API e processa os dados
        resposta = self.api_client.consultar_estoque_unidade(self.cnes_ativa)

        if resposta.get("success"):
            dados = resposta.get("data", [])
            estoque_filtrado = [i for i in dados if i.get(
                "slugprogramasaude") == "acaoJudicial"]

            for item in estoque_filtrado:
                tabela.insert("", END, values=(
                    item.get("lote"), item.get("codigosimpas"),
                    item.get("nomemedicamento"), item.get("quantidadeestoque")
                ))
        else:
            messagebox.showerror(
                "Erro", "Não foi possível carregar o estoque.")

        tabela.pack(expand=True, fill=BOTH)
