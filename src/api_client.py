import httpx


class ClienteAFSESAB:
    def __init__(self):
        self.base_url = "http://hotfix.afsesab.sesab.ba.gov.br"
        self.http_client = httpx.Client(base_url=self.base_url, timeout=15.0)

        # Variável de estado para guardar o JWT retornado no login
        self.token = None

    def autenticar(self, usuario: str, senha: str) -> bool:
        """
        Realiza o POST de login e armazena o token na instância da classe.
        """
        payload = {
            "email": usuario,
            "password": senha
        }

        try:
            response = self.http_client.post("/logistica/login", json=payload)

            if response.status_code == 200:
                dados = response.json()

                # Extrai o token da resposta da API do AFSESAB
                token_recebido = dados.get("token")

                if token_recebido:
                    # Salvamos o token na nossa classe explicitamente
                    self.token = token_recebido
                    return True

            print(
                f"[Aviso] Falha no login: {response.status_code} - {response.text}")
            return False

        except Exception as e:
            print(f"[Erro de Rede - Autenticação]: {e}")
            return False

    def consultar_estoque_unidade(self, cnes: str) -> dict:
        """
        Faz um GET na API do AFSESAB injetando o Token JWT no Header da requisição.
        """
        # 1. Validação Fail-Fast: Se não há token, nem gastamos rede fazendo a requisição
        if not self.token:
            print(
                "[Segurança] Tentativa de consulta bloqueada: Usuário sem token (não logado).")
            return {"success": False, "data": []}

        # 2. Montagem do Cabeçalho de Autenticação (Header)
        # O padrão de mercado para JWT é enviar como "Bearer <token>"
        # (Se a API do AFSESAB exigir outro nome, como "x-access-token", basta alterar a chave abaixo)
        headers_autenticados = {
            "Authorization": f"Bearer {self.token}"
        }

        try:
            # 3. Disparo do GET passando o header explicitamente
            response = self.http_client.get(
                f"/logistica/consultar-posicao-estoque?codigoAlmoxarifado={cnes}",
                headers=headers_autenticados
            )

            # 4. Tratamento das Respostas
            if response.status_code == 200:
                return response.json()

            elif response.status_code in (401, 403):
                # 401 Unauthorized / 403 Forbidden
                print(
                    "[Segurança] Token inválido ou expirado. O usuário precisa logar novamente.")
                # Aqui você poderia disparar um gatilho para a interface forçar o logout
                return {"success": False, "data": []}

            else:
                print(f"[Aviso] A API retornou status {response.status_code}")
                return {"success": False, "data": []}

        except Exception as e:
            print(f"[Erro de Rede - Estoque]: {e}")
            return {"success": False, "data": []}
