import lmstudio as lms

def agente_simples(prompt, texto, model):

    """
    Função que cria um agente simples para processar prompts e textos.
    :param prompt: O prompt do sistema (string)
    :param texto: O texto do usuário (string)
    :param model: O modelo de linguagem a ser usado
    """
    chat = lms.Chat()
    chat.add_system_prompt(prompt)
    # Envolver o texto em um bloco de código para evitar problemas de parsing
    mensagem_formatada = f"```\n{texto}\n```"
    chat.add_user_message(mensagem_formatada)

    resposta = model.respond(chat)
    resposta = str(resposta)
    chat = ""
    return resposta
