import grpc
import tarefas_pb2
import tarefas_pb2_grpc

def run():
    with grpc.insecure_channel('192.168.1.35:33021') as channel:
        stub = tarefas_pb2_grpc.GerenciadorDeTarefasStub(channel)

        while True:
            print("\n--- SISTEMA DE TAREFAS ---")
            print("1. Criar Tarefa")
            print("2. Listar Tarefas")
            print("3. Atualizar Tarefa")
            print("4. Deletar Tarefa")
            print("0. Sair")

            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                titulo = input("Título: ")
                desc = input("Descrição: ")
                data = input("Data Limite: ")
                resp = input("Responsável: ")

                resposta = stub.CriarTarefa(tarefas_pb2.TarefaRequest(
                    titulo=titulo, descricao=desc, data_limite=data, responsavel=resp
                ))
                print(f"\n{resposta.mensagem} ID: {resposta.tarefa.id}")

            elif opcao == '2':
                resposta = stub.ListarTarefas(tarefas_pb2.ListaRequest())
                print("\n--- LISTA DE TAREFAS ---")
                for t in resposta.tarefas:
                    print(f"ID: {t.id} | [{t.status}] {t.titulo} - Resp: {t.responsavel} (Até: {t.data_limite})")
                    print(f"    Descrição: {t.descricao}")
                    print("-" * 40)

            elif opcao == '3':
                id_t = input("ID da tarefa que deseja atualizar: ")
                titulo = input("Novo Título: ")
                desc = input("Nova Descrição: ")
                status = input("Novo Status (ex: Concluído): ")
                data = input("Nova Data Limite: ")
                resp = input("Novo Responsável: ")

                resposta = stub.AtualizarTarefa(tarefas_pb2.TarefaAtualizacaoRequest(
                    id=id_t, titulo=titulo, descricao=desc, status=status, data_limite=data, responsabil=resp
                ))
                print(f"\n{resposta.mensagem}")

            elif opcao == '4':
                id_t = input("ID da tarefa que deseja deletar: ")
                resposta = stub.DeletarTarefa(tarefas_pb2.DeletarRequest(id=id_t))
                print(f"\n{resposta.mensagem}")

            elif opcao == '0':
                break
            else:
                print("Opção inválida!")

if __name__ == '__main__':
    run()
