import re
import lmstudio as lms
from typing import Any
from duckling import conversor_pdf_simples
from a_gente import agente_simples
from prompts import PROMPT_EXTRAIR_COMPRAS, PROMPT_PROCESSAR_TABELA





def remove_thinking_tags(text: str) -> str:
    """
    Remove as tags <think> e </think> do texto, bem como quaisquer espaços em branco extras.
    :param text: O texto do modelo que pode conter as tags de pensamento (string)
    :return: O texto limpo sem as tags e pensamento (string)
    """
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    return re.sub(r'\s+', ' ', cleaned).strip()


def processar_pdf_com_modelo(caminho_pdf: str, model: Any) -> str:
    """
    Docstring for processar_pdf_com_modelo

    envia o documento ao docling para retirada da informação bruta,
    depois envia o resultado ao modelo com o prompt de extração de compras para organizar os dados em uma tabela csv.
    
    :param caminho_pdf: entrada do path do pdf (string)
    :param model: modelo a ser usado lmstudio (model)
    :return: resposta do modelo com a tabela processada (string)

    """
   
    
    resultado_doc = conversor_pdf_simples(caminho_pdf, extrair_imagens=True)
    print("Documento processado pelo conversor de PDF com sucesso.")
    print("Dado extraído do documento:\n********************************")
    print(f"\n\n{resultado_doc}\n********************************\n\n")
    resposta = agente_simples(PROMPT_EXTRAIR_COMPRAS, resultado_doc, model)
    resposta = remove_thinking_tags(resposta)
    print("**Resposta do modelo gerada com sucesso.**")
    

    return resposta


def processar_texto_tabela1(texto_tabela: str, model: Any) -> str:
    """
    Docstring for processar_texto_tabela1
    
    :param texto_tabela: entrada do texto da tabela (string)
    :param model: modelo a ser usado lmstudio (model)
    :return: resposta do modelo com a tabela processada (string)

    """
    
    resposta = agente_simples(PROMPT_PROCESSAR_TABELA, texto_tabela, model)
    resposta = remove_thinking_tags(resposta)
    print("**Resposta do modelo gerada com sucesso.**")
    
    return resposta












if __name__ == "__main__":
    model = lms.llm("qwen/qwen3-8b")
    caminho_pdf = "documents/nota1.pdf"
    tabela_notas = processar_pdf_com_modelo(caminho_pdf, model)
    print("Resposta tabela notas:\n********************************")
    print(f"\n\n{tabela_notas}\n********************************\n\n")
    tabela_produtos = processar_texto_tabela1(tabela_notas, model)
    print("Resposta tabela produtos:\n********************************")
    print(f"\n\n{tabela_produtos}\n********************************\n\n")