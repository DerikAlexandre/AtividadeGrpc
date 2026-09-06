from concurrent import futures
import os
import json
import uuid
import grpc
import tarefas_pb2
import tarefas_pb2_grpc

PASTA_DADOS = "dados_tarefas"

class ServenciadorDeTarefas(tarefas_pb2_grpc.GerenciadorDeTarefasServicer):

    def __init__(self):
        if not os.path.exists(PASTA_DADOS):
            os.makedirs(PASTA_DADOS)

    def CriarTarefa(self, request, context):
        id_tarefa = str(uuid.uuid4())
        tarefa_dict = {
            "id": id_tarefa,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": "Pendente",
            "data_limite": request.data_limite,
            "responsavel": request.responsavel
        }

        caminho_arquivo = os.path.join(PASTA_DADOS, f"{id_tarefa}.json")
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(tarefa_dict, f, ensure_ascii=False, indent=4)

        tarefa_proto = tarefas_pb2.Tarefa(**tarefa_dict)
        return tarefas_pb2.TarefaResponse(mensagem="Tarefa criada com sucesso!", tarefa=tarefa_proto)

    def ListarTarefas(self, request, context):
        tarefas = []
        for arquivo in os.listdir(PASTA_DADOS):
            if arquivo.endswith(".json"):
                caminho_arquivo = os.path.join(PASTA_DADOS, arquivo)
                with open(caminho_arquivo, "r", encoding="utf-8") as f:
                    tarefa_dict = json.load(f)
                    tarefas.append(tarefas_pb2.Tarefa(**tarefa_dict))

        return tarefas_pb2.ListaResponse(tarefas=tarefas)

    def AtualizarTarefa(self, request, context):
        caminho_arquivo = os.path.join(PASTA_DADOS, f"{request.id}.json")
        if not os.path.exists(caminho_arquivo):
            context.abort(grpc.StatusCode.NOT_FOUND, "Tarefa não encontrada.")

        tarefa_dict = {
            "id": request.id,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": request.status,
            "data_limite": request.data_limite,
            "responsavel": request.responsavel
        }

        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(tarefa_dict, f, ensure_ascii=False, indent=4)

        tarefa_proto = tarefas_pb2.Tarefa(**tarefa_dict)
        return tarefas_pb2.TarefaResponse(mensagem="Tarefa atualizada com sucesso!", tarefa=tarefa_proto)

    def DeletarTarefa(self, request, context):
        caminho_arquivo = os.path.join(PASTA_DADOS, f"{request.id}.json")
        if not os.path.exists(caminho_arquivo):
            return tarefas_pb2.DeletarResponse(mensagem="Tarefa não encontrada.", sucesso=False)

        os.remove(caminho_arquivo)
        return tarefas_pb2.DeletarResponse(mensagem="Tarefa deletada com sucesso!", sucesso=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tarefas_pb2_grpc.add_GerenciadorDeTarefasServicer_to_server(ServenciadorDeTarefas(), server)
    server.add_insecure_port('[::]:33021')
    server.start()
    print("Servidor gRPC rodando na porta 33021...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

