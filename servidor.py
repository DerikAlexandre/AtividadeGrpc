from concurrent import futures
import os
import json
import uuid
import grpc
import tarefas_pb2
import tarefas_pb2_grpc


PASTA = "dados_tarefas"


class GerenciadorDeTarefasServicer(
        tarefas_pb2_grpc.GerenciadorDeTarefasServicer):

    def __init__(self):
        if not os.path.exists(PASTA):
            os.makedirs(PASTA)

    def CriarTarefa(self, request, context):
        print(f"[REQ] Criando nova tarefa: '{request.titulo}'")

        id_novo = str(uuid.uuid4())

        dados = {
            "id": id_novo,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": "Pendente",
            "data_limite": request.data_limite,
            "responsavel": request.responsavel
        }

        caminho = os.path.join(PASTA, f"{id_novo}.json")

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        t_proto = tarefas_pb2.Tarefa(**dados)

        return tarefas_pb2.TarefaResponse(
            mensagem="Tarefa salva com sucesso!",
            tarefa=t_proto
        )

    def ListarTarefas(self, request, context):
        print("[REQ] Listando todas as tarefas...")

        lista = []

        for arq in os.listdir(PASTA):
            if arq.endswith(".json"):
                caminho = os.path.join(PASTA, arq)

                with open(caminho, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                    lista.append(tarefas_pb2.Tarefa(**dados))

        return tarefas_pb2.ListaResponse(tarefas=lista)

    def AtualizarTarefa(self, request, context):
        print(f"[REQ] Atualizando tarefa: {request.id}")

        caminho = os.path.join(PASTA, f"{request.id}.json")

        if not os.path.exists(caminho):
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Tarefa nao encontrada."
            )

        dados = {
            "id": request.id,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": request.status,
            "data_limite": request.data_limite,
            "responsavel": request.responsavel
        }

        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        t_proto = tarefas_pb2.Tarefa(**dados)

        return tarefas_pb2.TarefaResponse(
            mensagem="Tarefa atualizada!",
            tarefa=t_proto
        )

    def DeletarTarefa(self, request, context):
        print(f"[REQ] Deletando tarefa: {request.id}")

        caminho = os.path.join(PASTA, f"{request.id}.json")

        if not os.path.exists(caminho):
            return tarefas_pb2.DeletarResponse(
                mensagem="Tarefa nao encontrada.",
                sucesso=False
            )

        os.remove(caminho)

        return tarefas_pb2.DeletarResponse(
            mensagem="Tarefa removida com sucesso!",
            sucesso=True
        )


def iniciar_servidor():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    tarefas_pb2_grpc.add_GerenciadorDeTarefasServicer_to_server(
        GerenciadorDeTarefasServicer(),
        server
    )

    server.add_insecure_port("[::]:33021")
    server.start()

    print("=== Servidor gRPC rodando na porta 33021 ===")

    server.wait_for_termination()


if __name__ == "__main__":
    iniciar_servidor()