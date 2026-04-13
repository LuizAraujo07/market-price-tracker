import re
from typing import Any
from duckling import conversor_pdf_simples
from a_gente import agente_simples
from prompts import PROMPT_EXTRAIR_COMPRAS, PROMPT_PROCESSAR_TABELA, PROMPT_NOTA_JSON
from normalizador import parsear_csv





def remove_thinking_tags(text: str) -> str:
    """
    Docstring for remove_thinking_tags

    Remove as tags <think></think> e todo o conteúdo de pensamento entre elas.
    :param text: O texto do modelo que pode conter as tags de pensamento (string)
    :return: O texto limpo sem as tags e pensamento (string)
    """
    cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    cleaned = re.sub(r'<\|channel>.*?<channel\|>', '', cleaned, flags=re.DOTALL)
    return cleaned.strip()


def calcular_preco_por_kg(
    produto: str,
    quantidade: float,
    unidade: str,
    peso_unitario_g: str,
    preco_pago: float
) -> float | None:
    """
    Docstring for calcular_preco_por_kg

    Calcula o preço por kg do produto para permitir comparação justa entre embalagens diferentes.
    :param produto: nome do produto (string)
    :param quantidade: quantidade original (float)
    :param unidade: unidade de medida, ex: "UN", "KG" (string)
    :param peso_unitario_g: peso unitário em gramas extraído pelo modelo, ou "N/A" (string)
    :param preco_pago: valor total pago (float)
    :return: preço por kg (float) ou None se não for possível calcular
    """
    try:
        if unidade.upper() == "KG":
            # já está em kg, só divide
            return round(preco_pago / quantidade, 2)

        if unidade.upper() == "UN" and peso_unitario_g != "N/A":
            peso_kg = float(peso_unitario_g) / 1000
            quantidade_total_kg = quantidade * peso_kg
            return round(preco_pago / quantidade_total_kg, 2)

        # UN sem peso conhecido — não é possível calcular
        print(f"[AVISO] Não foi possível calcular preço/kg para '{produto}' — sem peso unitário.")
        return None

    except (ValueError, ZeroDivisionError) as e:
        print(f"[ERRO] Falha ao calcular preço/kg para '{produto}': {e}")
        return None


def processar_pdf_json(caminho_pdf: str, model: Any) -> str:
    """
    Docstring for processar_pdf_json
    
    :param caminho_pdf: entrada do path do pdf (string)
    :param model: modelo a ser usado lmstudio (model)
    :return: resposta do modelo com a tabela processada (string)

    """
    resultado_doc = conversor_pdf_simples(caminho_pdf, extrair_imagens=False)
    print("Documento processado pelo conversor de PDF com sucesso.")
    print("Dado extraído do documento:\n********************************")
    print(f"\n\n{resultado_doc}\n********************************\n\n")
    resposta = agente_simples(PROMPT_NOTA_JSON, resultado_doc, model)
    resposta = remove_thinking_tags(resposta)
    print("**Resposta do modelo gerada com sucesso.**")
    
    return resposta




def processar_pdf_com_modelo(caminho_pdf: str, model: Any) -> str:
    """
    Docstring for processar_pdf_com_modelo

    envia o documento ao docling para retirada da informação bruta,
    depois envia o resultado ao modelo com o prompt de extração de compras para organizar os dados em uma tabela csv.
    
    :param caminho_pdf: entrada do path do pdf (string)
    :param model: modelo a ser usado lmstudio (model)
    :return: resposta do modelo com a tabela processada (string)

    """
   
    
    resultado_doc = processar_pdf_json(caminho_pdf, model)

    print("iniciando processamento do json para tabela csv...  ")
    resposta = agente_simples(PROMPT_EXTRAIR_COMPRAS, resultado_doc, model)
    print("Resposta do modelo:\n********************************")
    print(f"\n\n{resposta}\n********************************\n\n")
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
    tabela_final = []
    tabela_em_linhas = parsear_csv(texto_tabela)

    for linha in tabela_em_linhas:
        resposta = agente_simples(PROMPT_PROCESSAR_TABELA, linha, model)
        resposta = remove_thinking_tags(resposta)
        tabela_final.append(resposta)

    print("**Resposta do modelo gerada com sucesso.**")
    
    return tabela_final

def processar_nota_tab1(texto_nota: str, model: Any) -> str:
    """
    Docstring for processar_nota_tab1
    
    :param texto_nota: entrada do texto da nota (string)
    :param model: modelo a ser usado lmstudio (model)
    :return: resposta do modelo com a tabela processada (string)

    """
    resposta = agente_simples(PROMPT_EXTRAIR_COMPRAS, texto_nota, model)
    # resposta = remove_thinking_tags(resposta)
    print("**Resposta do modelo gerada com sucesso.**")
    
    return resposta










if __name__ == "__main__":
    import lmstudio as lms
    model = lms.llm("nvidia/nemotron-3-nano-4b")
    caminho_pdf = "documents/nota1.pdf"
    tabela_notas = processar_pdf_com_modelo(caminho_pdf, model)
    print("Resposta tabela notas:\n********************************")
    print(f"\n\n{tabela_notas}\n********************************\n\n")
    tabela_produtos = processar_texto_tabela1(tabela_notas, model)
    print("Resposta tabela produtos:\n********************************")
    print(f"\n\n{tabela_produtos}\n********************************\n\n")