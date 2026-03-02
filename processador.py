import lmstudio as lms
from duckling import conversor_pdf_simples
from a_gente import agente_simples

# model = lms.llm("google/gemma-3-4b")
# caminho_pdf = "documents/nota1.pdf"

def processar_pdf_com_modelo(caminho_pdf, model):
    """
    Docstring for processar_pdf_com_modelo
    
    :param caminho_pdf: entrada do path do pdf (string)
    :param prompito: prompt para o modelo (string)
    """
    prompt = """Extraia os dados de compra do texto abaixo e organize-os em uma tabela. Seja estritamente objetivo e siga estas diretrizes:

1. **Estrutura da Tabela:** Nome do Produto | Valor Total | Quantidade | Unidade de Medida | Valor Unitário | Data da Compra | Local da Compra.
2. **Padronização:** Use o formato de data DD/MM/AAAA. Se o valor unitário não estiver explícito, calcule-o dividindo o valor total pela quantidade. Local de compra é o estabelecimento. nome do produto não vem com o código.
3. **Dados Ausentes:** Caso alguma informação não esteja disponível, preencha a célula com "N/A".
4. **Restrição:** Responda **apenas** com a tabela, sem introduções ou comentários adicionais.
"""
    
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
    prompt = """**Papel:** Você é um especialista em estruturação de dados e higienização de cadastros de compras.

**Objetivo:** Processar uma tabela de compras bruta, normalizando nomes de produtos, unidades de medida e quantidades.

**Instruções de Processamento:**

1. **Extração do Nome (Produto):**
* Remova marcas, pesos, tamanhos e adjetivos secundários.
* Mantenha apenas o nome essencial do item (ex: "Arroz", "Feijão", "Macarrão").


2. **Padronização de Unidade de Medida:**
* Identifique o peso/volume mencionado no texto original (ex: 500g, 1kg, 2L).
* Se a unidade original for "Unidade" mas o produto tiver peso/volume, altere para a unidade de massa ou volume correspondente (**kg**, **L**).


3. **Cálculo da Quantidade_Total:**
* Se a unidade de medida for alterada de "Unidade" para uma medida de peso/volume, multiplique a `Quantidade` original pelo valor unitário extraído da descrição.
* *Exemplo:* "2 unidades de Macarrão 500g" → `Unidade_Medida`: **kg** | `Quantidade_Total`: **1** (pois 2 * 0.5kg = 1kg).


4. **Saída de Dados:**
* Gere exclusivamente uma tabela Markdown com as colunas: `Produto`, `Quantidade_Total`, `Unidade_Medida`, `Preco_Pago`, `Data_Compra`.



**Restrição Estrita:** Não adicione saudações, explicações ou qualquer texto fora da tabela solicitada. Responda **apenas** com a tabela processada.
    """
    
    resposta = agente_simples(prompt, texto_tabela, model)
    print("Resposta do modelo gerada com sucesso.")
    
    return resposta













# tabela_notas = processar_pdf_com_modelo(caminho_pdf, model)
# print("Resposta tabela notas:\n********************************")
# print(f"\n\n{tabela_notas}\n********************************\n\n")
# tabela_produtos = processar_texto_tabela1(tabela_notas, model)
# print("Resposta tabela produtos:\n********************************")
# print(f"\n\n{tabela_produtos}\n********************************\n\n")