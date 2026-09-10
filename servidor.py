from concurrent import futures
import os
import json
import uuid
import grpc
import tarefas_pb2
import tarefas_pb2_grpc


DIRETORIO = "tarefas"


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

    print("Servidor gRPC na porta 33021...")

    server.wait_for_termination()


class GerenciadorDeTarefasServicer(tarefas_pb2_grpc.GerenciadorDeTarefasServicer):

    def __init__(self):
        if not os.path.exists(DIRETORIO):
            os.makedirs(DIRETORIO)

    def ListarTarefas(self, request, context):
        print("Buscando lista de tarefas...")

        elementos = []

        for arq in os.listdir(DIRETORIO):
            if arq.endswith(".json"):
                arquivo = os.path.join(DIRETORIO, arq)

                with open(arquivo, "r", encoding="utf-8") as f:
                    info = json.load(f)
                    elementos.append(tarefas_pb2.Tarefa(**info))

        return tarefas_pb2.ListaResponse(tarefas=elementos)

    def CriarTarefa(self, request, context):
        print(f"Salvando nova tarefa: '{request.titulo}'")

        novo_id = str(uuid.uuid4())

        info = {
            "id": novo_id,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": "Pendente",
            "data_limite": request.data_limite,
            "responsavel": request.responsavel,
            "prioridade": request.prioridade
        }

        arquivo = os.path.join(DIRETORIO, f"{novo_id}.json")

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=4)

        obj = tarefas_pb2.Tarefa(**info)

        return tarefas_pb2.TarefaResponse(
            mensagem="Tarefa salva!",
            tarefa=obj
        )

    def DeletarTarefa(self, request, context):
        print(f"Removendo o registro: {request.id}")

        arquivo = os.path.join(DIRETORIO, f"{request.id}.json")

        if not os.path.exists(arquivo):
            return tarefas_pb2.DeletarResponse(
                mensagem="Tarefa nao encontrada.",
                sucesso=False
            )

        os.remove(arquivo)

        return tarefas_pb2.DeletarResponse(
            mensagem="Tarefa removida!",
            sucesso=True
        )

    def AtualizarTarefa(self, request, context):
        print(f"Atualizando o registro: {request.id}")

        arquivo = os.path.join(DIRETORIO, f"{request.id}.json")

        if not os.path.exists(arquivo):
            context.abort(
                grpc.StatusCode.NOT_FOUND,
                "Tarefa nao encontrada."
            )

        info = {
            "id": request.id,
            "titulo": request.titulo,
            "descricao": request.descricao,
            "status": request.status,
            "data_limite": request.data_limite,
            "responsavel": request.responsavel,
            "prioridade": request.prioridade
        }

        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(info, f, ensure_ascii=False, indent=4)

        obj = tarefas_pb2.Tarefa(**info)

        return tarefas_pb2.TarefaResponse(
            mensagem="Tarefa atualizada!",
            tarefa=obj
        )


if __name__ == "__main__":
    iniciar_servidor()