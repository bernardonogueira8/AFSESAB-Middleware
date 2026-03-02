<div align="center">
  
# AFSESAB - Middleware

</div>

<div align="center">
  
[![Tech](https://skillicons.dev/icons?i=python,postgres,postman)](https://skillicons.dev)

</div>

_Resumo do Projeto: O AFSESAB Middleware é uma aplicação robusta desenvolvida em Python que atua como um nó logístico e interface gráfica desktop para unidades de saúde. Seu objetivo é realizar a interoperabilidade segura com a API do AFSESAB, otimizando a operação de ponta._

## Estrutura do Projeto

Aqui está a estrutura de diretórios ideal (no padrão src layout) para dividirmos o código do seu projeto:

```
src
├── init.py
├── main.py        # Responsável apenas pelo Login, Menu e Roteamento
├── api_client.py  # Gerencia a comunicação HTTP e o Token JWT
├── database.py    # Configura a conexão e a sessão (Engine) do PostgreSQL
├── models.py      # Contém as tabelas do SQLAlchemy (UnidadeLocal, paciente, etc.)
└── telas/         # Módulo dedicado aos componentes visuais
  ├── init.py
  ├── tela_estoque.py
  ├── tela_pacientes.py
  └── tela_recebimento.py
```

## 🤝 Colaboradores

Agradecemos às seguintes pessoas que contribuíram para este projeto:

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/bernardonogueira8">
        <img src="https://avatars.githubusercontent.com/u/62897976?s=400&u=afa8e717adda64a162c125cbbbcdfa187b86348a&v=4" width="160px;" alt="Foto do GitHub"/><br>
          <sub>
          <b>
          Bernardo Nogueira - bernardonogueira8
          </b>
        </sub>
      </a>
    </td>
  </tr>
</table>
