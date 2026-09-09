import grpc
import tarefas_pb2
import tarefas_pb2_grpc


def main():
    ip_servidor = input("Digite o IP do servidor: ").strip()

    if not ip_servidor:
        ip_servidor = "localhost"

    url = f"{ip_servidor}:33021"

    channel = grpc.insecure_channel(url)
    stub = tarefas_pb2_grpc.GerenciadorDeTarefasStub(channel)

    while True:
        print("\n=== MENU ===")
        print("1 Cadastrar tarefa")
        print("2 Listar todas as tarefas")
        print("3 Atualizar tarefas")
        print("4 Remover tarefa")
        print("0 Sair")

        op = input("Escolhas: ").strip()

        if op == "1":
            print("\n=== Novo cadastro ===")

            titulo = input("Titulo: ")
            desc = input("Descricao: ")
            data = input("Data limite: ")
            resp = input("Responsavel: ")

            dados = tarefas_pb2.TarefaRequest(
                titulo=titulo,
                descricao=desc,
                data_limite=data,
                responsavel=resp
            )

            res = stub.CriarTarefa(dados)

            print(f"\n>> {res.mensagem} (ID: {res.tarefa.id})")

        elif op == "2":
            dados = tarefas_pb2.ListaRequest()
            res = stub.ListarTarefas(dados)

            print("\n--- Lista das tarefas ---")

            if not res.tarefas:
                print("Nenhuma tarefa cadastrada até o momento.")

            for item in res.tarefas:
                print(f"ID: {item.id}")
                print(f"Titulo: {item.titulo} [{item.status}]")
                print(f"Responsavel: {item.responsavel} | Prazo: {item.data_limite}")
                print(f"Detalhes: {item.descricao}")
                print("-" * 35)

        elif op == "3":
            print("\n--- Atualizar Tarefa ---")

            id_t = input("ID da tarefa: ")
            titulo = input("Novo titulo: ")
            desc = input("Nova descricao: ")
            status = input("Novo status (ex: Concluido): ")
            data = input("Nova data limite: ")
            resp = input("Novo responsavel: ")

            dados = tarefas_pb2.TarefaAtualizacaoRequest(
                id=id_t,
                titulo=titulo,
                descricao=desc,
                status=status,
                data_limite=data,
                responsavel=resp
            )

            res = stub.AtualizarTarefa(dados)

            print(f"\n{res.mensagem}")

        elif op == "4":
            id_t = input("\nIDS para deletar: ")

            dados = tarefas_pb2.DeletarRequest(id=id_t)
            res = stub.DeletarTarefa(dados)

            print(f"\n{res.mensagem}")

        elif op == "0":
            print("Saindo.")
            break

        else:
            print("Opcao invalida!")


if __name__ == "__main__":
    main()
