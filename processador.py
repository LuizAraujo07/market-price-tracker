import lmstudio as lms
from duckling import conversor_pdf_simples
from a_gente import agente_simples

model = lms.llm("google/gemma-3-4b")
caminho_pdf = "documents/nota1.pdf"

def processar_pdf_com_modelo(caminho_pdf, model):
    """
    Docstring for processar_pdf_com_modelo
    
    :param caminho_pdf: entrada do path do pdf (string)
    :param prompito: prompt para o modelo (string)
    """
    prompt = """Separe apenas os dados importantes do texto e responda de forma objetiva. 
    Como produto final, gere uma tabela contendo nome do produto, valor total, quantidade, unidade de medida, valor unitario, data da compra, local da compra.
    Nao escreva mais nada alem disso."""
    
    resultado_markdown = conversor_pdf_simples(caminho_pdf, extrair_imagens=True)
    print("PDF convertido para Markdown com sucesso.")
    print("Documento convertido para Markdown:\n********************************")
    print(f"\n\n{resultado_markdown}\n********************************\n\n")
    resposta = agente_simples(prompt, resultado_markdown, model)
    print("Resposta do modelo gerada com sucesso.")
    

    return resposta

def processar_texto_tabela1(texto_tabela, model):
    """
    Docstring for processar_texto_tabela1
    
    :param texto_tabela: entrada do texto da tabela (string)
    :param model: modelo a ser usado lmstudio (model)
    """
    prompt = """Sera enviado a voce uma tabela com dados de compras. na coluna nome do produto pode ter a descrição completa do produto, incluindo marca, tamanho, peso e outras informações.
    Sua tarefa é extrair apenas o nome do produto, removendo todas as outras informações. por exemplo, se o nome do produto for "Arroz Tio João Tipo 1 Pacote 5kg", você deve extrair apenas "Arroz". 
    Tambem deve ser comparado se a unidade de medida esta de acodo com o nome do produto, por exemplo, se o nome do produto for "Feijão Carioca Pacote 1kg" e a unidade de medida for "Unidade", voce deve corrigir a unidade de medida para "kg".
    Verificar tambem se a quantidade vai estar de acordo com a nova medida corrigida, por exemplo, se a unidade de medida foi corrigida de "Unidade" para "kg" e a quantidade era 2 de "macarrão galo 500g" voce deve ajustar a quantidade para 1, pois se trata de 1kg de macarrão.
    Faça isso para todos os produtos na tabela.
    Gere uma nova tabela com as colunas: Produto, Quantidade_Total, Unidade_Medida, Preco_Pago, Data_Compra
    Nao escreva mais nada alem disso.
    """
    
    resposta = agente_simples(prompt, texto_tabela, model)
    print("Resposta do modelo gerada com sucesso.")
    
    return resposta













tabela_notas = processar_pdf_com_modelo(caminho_pdf, model)
print("Resposta tabela notas:\n********************************")
print(f"\n\n{tabela_notas}\n********************************\n\n")
tabela_produtos = processar_texto_tabela1(tabela_notas, model)
print("Resposta tabela produtos:\n********************************")
print(f"\n\n{tabela_produtos}\n********************************\n\n")