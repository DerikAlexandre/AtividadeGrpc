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
        print("\nMENU:")
        print("1 Cadastrar tarefa")
        print("2 Listar todas as tarefas")
        print("3 Atualizar tarefas")
        print("4 Remover tarefa")
        print("0 Sair")

        op = input("Escolhas: ").strip()

        if op == "1":
            print("\nNovo cadastro")

            titulo = input("Titulo: ")
            desc = input("Descricao: ")
            data = input("Data limite: ")
            resp = input("Responsavel: ")
            prioridade = input("Prioridade:")

            dados = tarefas_pb2.TarefaRequest(
                titulo=titulo,
                descricao=desc,
                data_limite=data,
                responsavel=resp,
                prioridade=prioridade
            )

            res = stub.CriarTarefa(dados)

            print(f"\nTarefa cadastrada! (ID: {res.tarefa.id})")

        elif op == "2":
            dados = tarefas_pb2.ListaRequest()
            res = stub.ListarTarefas(dados)

            print("\nLista das tarefas:")

            if not res.tarefas:
                print("Nenhuma tarefa cadastrada até o momento.")

            for item in res.tarefas:
                print(f"ID: {item.id}")
                print(f"Titulo: {item.titulo} [{item.status}]")
                print(f"Responsavel: {item.responsavel} | Prazo: {item.data_limite}")
                print(f"Detalhes: {item.descricao}")
                print(f"Prioridade: {item.prioridade}\n")

        elif op == "3":
            print("\nAtualizar Tarefa:")

            id_t = input("ID da tarefa: ")
            titulo = input("Novo titulo: ")
            desc = input("Nova descricao: ")
            status = input("Novo status (ex: Concluido): ")
            data = input("Nova data limite: ")
            resp = input("Novo responsavel: ")
            prioridade = input("Nova prioridade: ")

            dados = tarefas_pb2.TarefaAtualizacaoRequest(
                id=id_t,
                titulo=titulo,
                descricao=desc,
                status=status,
                data_limite=data,
                responsavel=resp,
                prioridade=prioridade
            )

            res = stub.AtualizarTarefa(dados)

            print(f"\nTarefa atualizada! (ID: {res.tarefa.id})")

        elif op == "4":
            id_t = input("\nIDS para deletar: ")

            dados = tarefas_pb2.DeletarRequest(id=id_t)
            res = stub.DeletarTarefa(dados)

            print(f"\nTarefa removida! (ID: {id_t})")

        elif op == "0":
            print("Saindo.")
            break

        else:
            print("Opcao invalida!")


if __name__ == "__main__":
    main()
