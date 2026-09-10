# Gerenciador de Tarefas com gRPC

**Membros da Equipe:**
* Derik Alexandre Alves de Andrade
* Maria Eugenia C. G. da Silva
* Aline de Brito Sério
* Felipe

---

## O que é este projeto?
Este é um sistema Cliente-Servidor via **gRPC** para o gerenciamento de tarefas. O sistema permite realizar operações de Criar, Listar, Atualizar e Deletar tarefas. Os dados são salvos e isolados diretamente no servidor no formato `.json`.

## Como Inicializar (Passo a Passo)

### 1. Preparar o Ambiente
Certifique-se de ter o Python instalado em sua máquina. Abra o terminal e instale as bibliotecas necessárias para o gRPC:
```bash
pip install grpcio grpcio-tools
```

### 2. Compilar o Protobuf
Caso os arquivos gerados pelo gRPC (`tarefas_pb2.py` e `tarefas_pb2_grpc.py`) ainda não estejam na pasta, será necessário gerar utilizando o arquivo instalado.
* Salve o código fornecido em um arquivo chamado `tarefas.proto`.
* Rode o seguinte comando:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. tarefas.proto
```

### 3. Iniciar o Servidor
Abra o terminal na pasta onde os arquivos estão localizados e inicie o servidor:
```bash
python servidor.py
```
* **Status:** O servidor começará a rodar na porta `33021` e criará automaticamente a pasta `dados_tarefas` para armazenar os arquivos `.json`. Não feche este terminal.

### 4. Iniciar o Cliente
Abra um **novo terminal** (mantendo o do servidor aberto) e inicie o script do cliente:
```bash
python cliente.py
```
* **Conexão:** O sistema solicitará o IP do servidor (caso seja ineserido o ip errado não será possivel cadastrar a tafera).
* **Uso:** Um menu interativo aparecerá na tela. Basta digitar a opção desejada (1 a 4) para interagir com o gerenciador de tarefas. Será criado uma pasta com os dados das tarefas cadastradas num arquivo chamado taferas.txt.